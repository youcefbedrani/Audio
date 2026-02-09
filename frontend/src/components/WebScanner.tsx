"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { createWorker, Worker } from "tesseract.js";
import { X, Camera, RefreshCw } from "lucide-react";

interface WebScannerProps {
    onScan: (result: string) => void;
    onClose: () => void;
    isEmbedded?: boolean;
}

export default function WebScanner({ onScan, onClose, isEmbedded = false }: WebScannerProps) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const workerRef = useRef<Worker | null>(null);
    const [isScanning, setIsScanning] = useState(false);
    const [initializing, setInitializing] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const streamRef = useRef<MediaStream | null>(null);
    const scanIntervalRef = useRef<NodeJS.Timeout | null>(null);

    // Initialize Tesseract worker
    useEffect(() => {
        const initWorker = async () => {
            try {
                const worker = await createWorker('eng');

                // Configure for the specific ID format (letters, numbers, #)
                await worker.setParameters({
                    tessedit_char_whitelist: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#',
                });

                workerRef.current = worker;
                setInitializing(false);
                startCamera();
            } catch (err) {
                console.error("Failed to initialize OCR:", err);
                setError("Failed to load text recognition.");
                setInitializing(false);
            }
        };

        initWorker();

        return () => {
            stopScanning();
            if (workerRef.current) {
                workerRef.current.terminate();
            }
        };
    }, []);

    const startCamera = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    facingMode: "environment",
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            });

            streamRef.current = stream;

            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                videoRef.current.onloadedmetadata = () => {
                    videoRef.current?.play();
                    setIsScanning(true);
                    startScanningLoop();
                };
            }
        } catch (err) {
            console.error("Camera error:", err);
            setError("Could not access camera. Please allow permissions.");
        }
    };

    const stopScanning = () => {
        if (scanIntervalRef.current) {
            clearInterval(scanIntervalRef.current);
            scanIntervalRef.current = null;
        }

        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
            streamRef.current = null;
        }

        setIsScanning(false);
    };

    const processFrame = async () => {
        if (!videoRef.current || !canvasRef.current || !workerRef.current || !isScanning) return;

        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        if (!ctx) return;

        // Draw only the center portion (the scan box) to the canvas for processing
        // The scan box is roughly 60% width and 20% height of the screen in the middle
        const scanWidth = video.videoWidth * 0.7;
        const scanHeight = video.videoHeight * 0.2;
        const startX = (video.videoWidth - scanWidth) / 2;
        const startY = (video.videoHeight - scanHeight) / 2;

        canvas.width = scanWidth;
        canvas.height = scanHeight;

        // Draw the video frame to the canvas (only the relevant crop)
        ctx.drawImage(
            video,
            startX, startY, scanWidth, scanHeight,
            0, 0, scanWidth, scanHeight
        );

        // Pre-process image for better OCR (Essential for Yellow text on Black background)
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;

        for (let i = 0; i < data.length; i += 4) {
            // Convert to grayscale
            const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;

            // Invert colors: Tesseract prefers dark text on light background
            // The product has Light (Yellow) text on Dark (Black) background.
            // Inverting makes it Dark (Blue/Grey) on Light (White).
            const value = 255 - avg;

            // Apply high contrast threshold
            // If original was bright (Yellow) -> avg is high -> value is low (Dark)
            // If original was dark (Black) -> avg is low -> value is high (Light)
            // Threshold at 100 seems reasonable for high contrast yellow/black
            const threshold = value < 100 ? 0 : 255;

            data[i] = threshold;     // R
            data[i + 1] = threshold; // G
            data[i + 2] = threshold; // B
        }
        ctx.putImageData(imageData, 0, 0);

        try {
            // Recognize text
            const { data: { text } } = await workerRef.current.recognize(canvas);

            // Clean and validate text
            const cleanText = text.replace(/[^A-Z0-9#]/g, '').trim();

            // Allow IDs with or without hash, length check usually roughly 10-20 known from example
            // Example scanned: #396A0C84B8914D2
            const match = cleanText.match(/#?[A-F0-9]{10,}/);

            if (match) {
                const foundId = match[0];
                console.log("OCR Match:", foundId);
                onScan(foundId);
                stopScanning();
            }
        } catch (err) {
            // Silent error on individual frame process
        }
    };

    const startScanningLoop = () => {
        if (scanIntervalRef.current) clearInterval(scanIntervalRef.current);
        // Scan every 500ms to balance performance and speed
        scanIntervalRef.current = setInterval(processFrame, 500);
    };

    return (
        <div className={`relative ${isEmbedded ? 'h-[400px] w-full rounded-xl overflow-hidden' : 'fixed inset-0 z-50 bg-black'}`}>
            {!isEmbedded && (
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 z-20 p-2 bg-white/20 backdrop-blur-md text-white rounded-full hover:bg-white/30"
                >
                    <X size={24} />
                </button>
            )}

            {/* Hidden canvas for processing */}
            <canvas ref={canvasRef} className="hidden" />

            <div className="relative w-full h-full flex flex-col items-center justify-center bg-black">
                {error ? (
                    <div className="text-white text-center p-6 bg-red-900/50 rounded-xl mx-4">
                        <p className="mb-4">{error}</p>
                        <button
                            onClick={() => window.location.reload()}
                            className="px-4 py-2 bg-white text-red-900 rounded-lg font-bold"
                        >
                            <RefreshCw className="inline mr-2 w-4 h-4" />
                            Retry
                        </button>
                    </div>
                ) : (
                    <>
                        {/* Video Feed */}
                        <video
                            ref={videoRef}
                            playsInline
                            muted
                            className="absolute inset-0 w-full h-full object-cover"
                        />

                        {/* Dark Overlay with Transparent Center */}
                        <div className="absolute inset-0 border-[50px] border-black/60 z-10 pointer-events-none">
                            {/* This creates a frame, but let's use a better CSS approach for the cut-out */}
                        </div>

                        {/* Proper Cut-out Overlay */}
                        <div className="absolute inset-0 z-10 flex flex-col items-center justify-center">
                            <div className="w-full h-1/3 bg-black/90 backdrop-blur-sm"></div>
                            <div className="w-full h-[150px] flex">
                                <div className="w-8 bg-black/90 backdrop-blur-sm"></div>
                                <div className="flex-1 relative border-2 border-yellow-400 rounded-lg shadow-[0_0_0_9999px_rgba(0,0,0,0.9)]">
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        {initializing && <RefreshCw className="w-8 h-8 text-yellow-400 animate-spin" />}
                                    </div>
                                    {/* Scan Line Animation */}
                                    <div className="absolute top-0 left-0 w-full h-0.5 bg-yellow-400 shadow-[0_0_10px_#FACC15] animate-[scan_2s_ease-in-out_infinite] opacity-70"></div>
                                </div>
                                <div className="w-8 bg-black/90 backdrop-blur-sm"></div>
                            </div>
                            <div className="w-full h-1/3 bg-black/90 backdrop-blur-sm flex flex-col items-center pt-8">
                                <p className="text-white/90 font-bold text-lg font-arabic shadow-black drop-shadow-md">وجه الكاميرا نحو الكود</p>
                                <p className="text-white/60 text-sm mt-1 font-arabic">#396A... مثال: </p>
                            </div>
                        </div>
                    </>
                )}
            </div>

            <style jsx>{`
                @keyframes scan {
                    0% { top: 0%; opacity: 0; }
                    10% { opacity: 1; }
                    90% { opacity: 1; }
                    100% { top: 100%; opacity: 0; }
                }
            `}</style>
        </div>
    );
}
