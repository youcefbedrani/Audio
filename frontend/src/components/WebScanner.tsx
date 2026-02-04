"use client";

import { useEffect, useRef, useState } from "react";
import { Html5Qrcode } from "html5-qrcode";
import { X, Camera } from "lucide-react";

interface WebScannerProps {
    onScan: (result: string) => void;
    onClose: () => void;
    isEmbedded?: boolean;
}

export default function WebScanner({ onScan, onClose, isEmbedded = false }: WebScannerProps) {
    const scannerRef = useRef<Html5Qrcode | null>(null);
    const [isScanning, setIsScanning] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const hasScannedRef = useRef(false);

    useEffect(() => {
        console.log("WebScanner: Component mounted");

        // Wait for DOM to be ready
        const initScanner = async () => {
            try {
                // Ensure the element exists
                const element = document.getElementById("qr-reader");
                if (!element) {
                    console.error("WebScanner: qr-reader element not found");
                    setError("Scanner element not found");
                    return;
                }

                console.log("WebScanner: Initializing Html5Qrcode");
                const scanner = new Html5Qrcode("qr-reader");
                scannerRef.current = scanner;

                await startScanning();
            } catch (err) {
                console.error("WebScanner: Initialization error:", err);
                setError("Failed to initialize scanner");
            }
        };

        // Small delay to ensure DOM is ready
        const timer = setTimeout(initScanner, 100);

        return () => {
            clearTimeout(timer);
            console.log("WebScanner: Component unmounting");
            stopScanning();
        };
    }, []);

    const startScanning = async () => {
        if (!scannerRef.current) {
            console.error("WebScanner: Scanner ref is null");
            return;
        }

        try {
            console.log("WebScanner: Starting camera...");
            setIsScanning(true);
            setError(null);

            await scannerRef.current.start(
                { facingMode: "environment" },
                {
                    fps: 10,
                    qrbox: { width: 250, height: 250 },
                },
                (decodedText) => {
                    // Prevent multiple scans
                    if (hasScannedRef.current) {
                        console.log("WebScanner: Already scanned, ignoring duplicate");
                        return;
                    }

                    hasScannedRef.current = true;
                    console.log("WebScanner: QR Code detected:", decodedText);
                    console.log("WebScanner: Calling onScan callback");

                    // Stop scanning first
                    stopScanning().then(() => {
                        console.log("WebScanner: Scanner stopped, triggering onScan");
                        onScan(decodedText);
                    });
                },
                (errorMessage) => {
                    // Ignore continuous scanning errors
                }
            );

            console.log("WebScanner: Camera started successfully");
        } catch (err: any) {
            console.error("WebScanner: Failed to start camera:", err);
            setError(`Camera error: ${err.message || "Please check permissions"}`);
            setIsScanning(false);
        }
    };

    const stopScanning = async () => {
        if (scannerRef.current) {
            try {
                if (scannerRef.current.isScanning) {
                    console.log("WebScanner: Stopping scanner...");
                    await scannerRef.current.stop();
                    console.log("WebScanner: Scanner stopped");
                }
                await scannerRef.current.clear();
                console.log("WebScanner: Scanner cleared");
            } catch (err) {
                console.error("WebScanner: Error stopping scanner:", err);
            }
        }
        setIsScanning(false);
    };

    return (
        <div className={`relative ${isEmbedded ? '' : 'fixed inset-0 z-50 bg-black'}`}>
            {!isEmbedded && (
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 z-10 p-2 bg-white rounded-full shadow-lg hover:bg-gray-100"
                >
                    <X size={24} />
                </button>
            )}

            <div className="flex flex-col items-center justify-center h-full p-4">
                <div id="qr-reader" className="w-full max-w-md rounded-lg overflow-hidden shadow-2xl"></div>

                {error && (
                    <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg max-w-md">
                        <p className="font-bold">Error</p>
                        <p>{error}</p>
                        <button
                            onClick={() => {
                                setError(null);
                                hasScannedRef.current = false;
                                startScanning();
                            }}
                            className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                        >
                            Retry
                        </button>
                    </div>
                )}

                {isScanning && !error && (
                    <div className="mt-4 text-white text-center">
                        <Camera className="w-8 h-8 mx-auto mb-2 animate-pulse" />
                        <p>Point camera at QR code</p>
                        <p className="text-sm text-gray-400 mt-2">Scanning...</p>
                    </div>
                )}
            </div>
        </div>
    );
}
