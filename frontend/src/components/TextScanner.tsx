"use client";

import { useRef, useState, useEffect } from "react";
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

    const workerRef = useRef<Tesseract.Worker | null>(null);
    const [isWorkerReady, setIsWorkerReady] = useState(false);

    // Initialize Tesseract worker
    useEffect(() => {
        const initWorker = async () => {
            try {
                console.log("TextScanner: Initializing Tesseract worker...");
                const worker = await Tesseract.createWorker("eng", 1, {
                    logger: m => {
                        if (m.status === "recognizing text" && (m.progress * 100) % 20 === 0) {
                            console.log(`TextScanner: Init Progress ${Math.round(m.progress * 100)}%`);
                        }
                    }
                });

                await worker.setParameters({
                    tessedit_char_whitelist: '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                });

                workerRef.current = worker;
                setIsWorkerReady(true);
                console.log("TextScanner: Worker ready");
            } catch (err) {
                console.error("TextScanner: Failed to init worker:", err);
                setError("Failed to initialize OCR engine");
            }
        };

        initWorker();

        return () => {
            if (workerRef.current) {
                console.log("TextScanner: Terminating worker");
                workerRef.current.terminate();
            }
        };
    }, []);

    const startContinuousScanning = () => {
        const interval = setInterval(async () => {
            if (!isScanning || isProcessing || !isWorkerReady) return;

            await captureAndRecognize();
        }, 800); // Scan every 800ms

        return () => clearInterval(interval);
    };

    const captureAndRecognize = async () => {
        if (!videoRef.current || !canvasRef.current || isProcessing || !workerRef.current) return;

        setIsProcessing(true);
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const context = canvas.getContext("2d");

        if (!context) return;

        // Define ROI (Region of Interest) - Center strip
        // Height: 30% of video height, centered
        const roiHeight = video.videoHeight * 0.3;
        const roiY = (video.videoHeight - roiHeight) / 2;

        // Set canvas size to ROI size
        canvas.width = video.videoWidth;
        canvas.height = roiHeight;

        // Draw only the ROI from video to canvas
        context.drawImage(
            video,
            0, roiY, video.videoWidth, roiHeight, // Source rect
            0, 0, canvas.width, canvas.height     // Dest rect
        );

        // Image Preprocessing for better OCR on yellow/black text
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;

        for (let i = 0; i < data.length; i += 4) {
            // Convert to grayscale
            const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;

            // Invert colors (make dark background light, loop text dark)
            // Tesseract prefers dark text on light background
            // Current: Yellow (Light) on Black (Dark).
            // Inverted: Blue (Dark) on White (Light).
            // Thresholding can improve further:
            const value = 255 - avg; // Invert

            // Apply high contrast threshold
            // If it was bright (Yellow), it becomes dark (low value).
            // If it was dark (Black), it becomes bright (high value).
            const threshold = value < 100 ? 0 : 255;

            data[i] = threshold;     // R
            data[i + 1] = threshold; // G
            data[i + 2] = threshold; // B
        }
        context.putImageData(imageData, 0, 0);

        try {
            // console.log("TextScanner: Recognizing text...");
            const worker = workerRef.current;
            const result = await worker.recognize(canvas);

            const confidence = result.data.confidence;
            // console.log(`TextScanner: Confidence ${confidence}`);

            if (confidence < 50) return;

            // Clean text: remove all non-alphanumeric except maybe needed special chars
            // Tesseract can be configured with whitelist, but post-processing is also good.
            const text = result.data.text.trim();
            // console.log("TextScanner: Recognized text:", text);

            // The ID format seems to be Hex-like: 396A0C84B8914D2 (15 chars)
            // It might contain O vs 0 confusion, or I vs 1.
            // Require at least 12 chars to avoid partial scans
            const idPattern = /[A-Z0-9]{12,}/gi;
            const matches = text.match(idPattern);

            if (matches && matches.length > 0) {
                // Get the longest match as it's likely the ID
                const detectedId = matches.reduce((a, b) => a.length > b.length ? a : b);
                console.log("TextScanner: Detected ID:", detectedId);

                // Basic validation: Hex usually
                if (detectedId.length >= 12) {
                    // Check if it's different enough or just valid
                    // Avoid duplicate scans if it's the SAME as last time
                    if (detectedId !== lastScannedText) {
                        setLastScannedText(detectedId);
                        stopCamera();
                        onScan(detectedId);
                    }
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
                    <div className="absolute inset-0 border-4 border-blue-500 pointer-events-none opacity-50"></div>

                    {/* Focus Area Guide */}
                    <div className="absolute top-1/2 left-0 right-0 h-32 -mt-16 border-y-2 border-yellow-400 bg-white/5 pointer-events-none flex items-center justify-center">
                        <div className="absolute inset-0 animate-pulse bg-yellow-400/10"></div>
                        <p className="text-yellow-400 text-xs font-bold bg-black/50 px-2 py-1 rounded">ضع الكود هنا</p>
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
