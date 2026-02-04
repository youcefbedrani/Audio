"use client";

import { useEffect, useRef } from "react";

interface WaveformVisualizerProps {
    stream?: MediaStream;
    audioUrl?: string;
    isPlaying?: boolean;
    color?: string;
    height?: number;
}

export default function WaveformVisualizer({
    stream,
    audioUrl,
    isPlaying,
    color = "#000000",
    height = 100,
}: WaveformVisualizerProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const animationRef = useRef<number>(undefined);
    const analyserRef = useRef<AnalyserNode>(undefined);
    const audioContextRef = useRef<AudioContext>(undefined);
    const sourceRef = useRef<MediaStreamAudioSourceNode | MediaElementAudioSourceNode>(undefined);

    useEffect(() => {
        if (!canvasRef.current) return;

        if (!audioContextRef.current) {
            audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
        }

        const audioContext = audioContextRef.current;

        // Clean up previous source/analyser
        if (sourceRef.current) {
            sourceRef.current.disconnect();
        }

        const analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        analyserRef.current = analyser;

        if (stream) {
            const source = audioContext.createMediaStreamSource(stream);
            source.connect(analyser);
            sourceRef.current = source;
            draw();
        } else if (audioUrl) {
            // Ideally we would fetch and decode audio data for a static visualization
            // For now, let's just leave this empty or implement a simple player visualization if needed
            // But for the scope of "Recording", stream is key. 
            // If we want to visualize a specific file, we might need to decode it.
        }

        return () => {
            cancelAnimationFrame(animationRef.current!);
            // audioContext.close(); // Don't close context aggressively in React double-render
        };
    }, [stream, audioUrl]);

    const draw = () => {
        if (!canvasRef.current || !analyserRef.current) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        const bufferLength = analyserRef.current.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        const renderFrame = () => {
            animationRef.current = requestAnimationFrame(renderFrame);
            analyserRef.current!.getByteFrequencyData(dataArray);

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const barWidth = (canvas.width / bufferLength) * 2.5;
            let barHeight;
            let x = 0;

            for (let i = 0; i < bufferLength; i++) {
                barHeight = dataArray[i] / 2;

                ctx.fillStyle = color;
                // Center the bars vertically
                const y = (canvas.height - barHeight) / 2;

                // Draw rounded bars
                roundRect(ctx, x, y, barWidth, barHeight, 2);

                x += barWidth + 1;
            }
        };

        renderFrame();
    };

    // Helper for rounded rects
    function roundRect(ctx: CanvasRenderingContext2D, x: number, y: number, w: number, h: number, r: number) {
        if (w < 2 * r) r = w / 2;
        if (h < 2 * r) r = h / 2;
        if (h < 1) return; // Don't draw tiny bars

        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.arcTo(x + w, y, x + w, y + h, r);
        ctx.arcTo(x + w, y + h, x, y + h, r);
        ctx.arcTo(x, y + h, x, y, r);
        ctx.arcTo(x, y, x + w, y, r);
        ctx.closePath();
        ctx.fill();
    }

    return (
        <canvas
            ref={canvasRef}
            width={600}
            height={height}
            className="w-full h-full"
        />
    );
}
