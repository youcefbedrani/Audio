"use client";

import { useRef, useState } from "react";
import { Camera, Loader2, X } from "lucide-react";
import Tesseract from "tesseract.js";

interface TextScannerProps {
    onScan: (text: string) => void;
    onClose: () => void;
}

export default function TextScanner({ onScan, onClose }: TextScannerProps) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const streamRef = useRef<MediaStream | null>(null);
    const [isScanning, setIsScanning] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [lastScannedText, setLastScannedText] = useState<string>("");

    const startCamera = async () => {
        try {
            console.log("TextScanner: Starting camera...");
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: "environment" },
            });

            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                streamRef.current = stream;
                setIsScanning(true);
                console.log("TextScanner: Camera started");

                // Start continuous scanning
                startContinuousScanning();
            }
        } catch (err: any) {
            console.error("TextScanner: Camera error:", err);
            setError(`Camera error: ${err.message}`);
        }
    };

    const startContinuousScanning = () => {
        const interval = setInterval(async () => {
            if (!isScanning || isProcessing) return;

            await captureAndRecognize();
        }, 2000); // Scan every 2 seconds

        return () => clearInterval(interval);
    };

    const captureAndRecognize = async () => {
        if (!videoRef.current || !canvasRef.current || isProcessing) return;

        setIsProcessing(true);
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");

        if (!context) return;

        // Set canvas size to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Draw current video frame to canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        try {
            console.log("TextScanner: Recognizing text...");

            const result = await Tesseract.recognize(canvas, "eng", {
                logger: (m) => {
                    if (m.status === "recognizing text") {
                        console.log(`TextScanner: Progress ${Math.round(m.progress * 100)}%`);
                    }
                },
            });

            const text = result.data.text.trim();
            console.log("TextScanner: Recognized text:", text);

            // Extract alphanumeric sequences that look like IDs
            const idPattern = /[A-Z0-9]{10,}/g;
            const matches = text.match(idPattern);

            if (matches && matches.length > 0) {
                const detectedId = matches[0];
                console.log("TextScanner: Detected ID:", detectedId);

                // Avoid duplicate scans
                if (detectedId !== lastScannedText) {
                    setLastScannedText(detectedId);
                    stopCamera();
                    onScan(detectedId);
                }
            }
        } catch (err) {
            console.error("TextScanner: OCR error:", err);
        } finally {
            setIsProcessing(false);
        }
    };

    const stopCamera = () => {
        console.log("TextScanner: Stopping camera...");
        if (streamRef.current) {
            streamRef.current.getTracks().forEach((track) => track.stop());
            streamRef.current = null;
        }
        setIsScanning(false);
    };

    const handleCapture = async () => {
        await captureAndRecognize();
    };

    // Start camera on mount
    useState(() => {
        startCamera();
    });

    return (
        <div className="relative w-full max-w-md">
            <button
                onClick={() => {
                    stopCamera();
                    onClose();
                }}
                className="absolute top-2 right-2 z-10 p-2 bg-white rounded-full shadow-lg hover:bg-gray-100"
            >
                <X size={20} />
            </button>

            <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
                <div className="relative">
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        muted
                        className="w-full h-64 object-cover bg-black"
                    />
                    <canvas ref={canvasRef} className="hidden" />

                    {/* Scanning overlay */}
                    <div className="absolute inset-0 border-4 border-blue-500 pointer-events-none">
                        <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-blue-500 animate-pulse"></div>
                    </div>

                    {isProcessing && (
                        <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                            <Loader2 className="w-8 h-8 text-white animate-spin" />
                        </div>
                    )}
                </div>

                <div className="p-4 text-center">
                    <p className="text-sm text-stone-600 mb-3 font-arabic">
                        وجه الكاميرا نحو رقم الإطار
                    </p>

                    {error && (
                        <div className="mb-3 p-2 bg-red-100 border border-red-300 text-red-700 rounded text-sm">
                            {error}
                        </div>
                    )}

                    <button
                        onClick={handleCapture}
                        disabled={isProcessing || !isScanning}
                        className="w-full py-3 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        {isProcessing ? (
                            <>
                                <Loader2 className="w-5 h-5 animate-spin" />
                                جاري المسح...
                            </>
                        ) : (
                            <>
                                <Camera className="w-5 h-5" />
                                مسح الآن
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}
