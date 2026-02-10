"use client";

import { useEffect, useRef, useState } from "react";
import { createWorker, Worker } from "tesseract.js";
import { X, RefreshCw, Zap } from "lucide-react";

interface UnifiedScannerProps {
    onScan: (result: string) => void;
    onClose: () => void;
    isEmbedded?: boolean;
}

export default function UnifiedScanner({ onScan, onClose, isEmbedded = false }: UnifiedScannerProps) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const workerRef = useRef<Worker | null>(null);
    const [isScanning, setIsScanning] = useState(false);
    const [initializing, setInitializing] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const streamRef = useRef<MediaStream | null>(null);
    const scanIntervalRef = useRef<NodeJS.Timeout | null>(null);
    const lastScanRef = useRef<string>("");
    const lastScanTimeRef = useRef<number>(0);

    // Initialize Tesseract worker for OCR
    useEffect(() => {
        const initWorker = async () => {
            try {
                const worker = await createWorker('eng');
                await worker.setParameters({
                    tessedit_char_whitelist: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                    tessedit_pageseg_mode: '7', // Single line mode for faster processing
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
        if (!videoRef.current || !canvasRef.current || !isScanning || !workerRef.current) return;

        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        if (!ctx) return;

        // Optimized scan area: 35% width, 12% height (very small for speed)
        const scanWidth = video.videoWidth * 0.35;
        const scanHeight = video.videoHeight * 0.12;
        const startX = (video.videoWidth - scanWidth) / 2;
        const startY = (video.videoHeight - scanHeight) / 2;

        canvas.width = scanWidth;
        canvas.height = scanHeight;

        ctx.drawImage(
            video,
            startX, startY, scanWidth, scanHeight,
            0, 0, scanWidth, scanHeight
        );

        // Aggressive preprocessing for maximum OCR speed and accuracy
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;

        for (let i = 0; i < data.length; i += 4) {
            const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
            const value = 255 - avg; // Invert
            const threshold = value < 120 ? 0 : 255; // Adjusted threshold
            data[i] = data[i + 1] = data[i + 2] = threshold;
        }
        ctx.putImageData(imageData, 0, 0);

        try {
            const { data: { text } } = await workerRef.current.recognize(canvas);
            const cleanText = text.replace(/[^A-Z0-9]/g, '').trim();

            // Match IDs: 10+ alphanumeric characters
            const match = cleanText.match(/[A-F0-9]{10,}/);

            if (match && !isDuplicate(match[0])) {
                console.log("ID detected:", match[0]);
                onScan(match[0]);
                stopScanning();
            }
        } catch (err) {
            // Silent error on individual frame
        }
    };

    const isDuplicate = (scannedData: string): boolean => {
        const now = Date.now();
        const DEBOUNCE_MS = 1000; // 1 second cooldown

        if (scannedData === lastScanRef.current && now - lastScanTimeRef.current < DEBOUNCE_MS) {
            return true;
        }

        lastScanRef.current = scannedData;
        lastScanTimeRef.current = now;
        return false;
    };

    const startScanningLoop = () => {
        if (scanIntervalRef.current) clearInterval(scanIntervalRef.current);
        // Very fast scan interval: 200ms for optimal speed/accuracy balance
        scanIntervalRef.current = setInterval(processFrame, 200);
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

            {/* Fast Scan Indicator */}
            <div className="absolute top-4 left-4 z-20 px-3 py-1 bg-black/60 backdrop-blur-md text-white rounded-full text-xs font-bold flex items-center gap-1">
                <Zap size={14} className="text-yellow-400" />
                Fast Scan
            </div>

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
                        <video
                            ref={videoRef}
                            playsInline
                            muted
                            className="absolute inset-0 w-full h-full object-cover"
                        />

                        {/* Optimized scan area overlay */}
                        <div className="absolute inset-0 z-10 flex flex-col items-center justify-center">
                            <div className="w-full h-[38%] bg-black/90 backdrop-blur-sm"></div>
                            <div className="w-full h-[100px] flex">
                                <div className="w-[20%] bg-black/90 backdrop-blur-sm"></div>
                                <div className="flex-1 relative border-2 border-yellow-400 rounded-lg shadow-[0_0_0_9999px_rgba(0,0,0,0.9)]">
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        {initializing && <RefreshCw className="w-8 h-8 text-yellow-400 animate-spin" />}
                                    </div>
                                    {/* Fast scan line animation */}
                                    <div className="absolute top-0 left-0 w-full h-0.5 bg-yellow-400 shadow-[0_0_10px_#FACC15] animate-[scan_1s_ease-in-out_infinite] opacity-70"></div>
                                </div>
                                <div className="w-[20%] bg-black/90 backdrop-blur-sm"></div>
                            </div>
                            <div className="w-full h-[38%] bg-black/90 backdrop-blur-sm flex flex-col items-center pt-8">
                                <p className="text-white/90 font-bold text-lg font-arabic shadow-black drop-shadow-md">وجه الكاميرا نحو رقم الإطار</p>
                                <p className="text-white/60 text-sm mt-1 font-arabic">396A0C84B8914D2 :مثال</p>
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
