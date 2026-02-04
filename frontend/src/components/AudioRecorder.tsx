"use client";

import { useState, useRef, useEffect } from "react";
import WaveformVisualizer from "./WaveformVisualizer";
import { Mic, Square, Trash2, Upload, Play, Pause } from "lucide-react";
import type { AudioData } from "../lib/types";

interface AudioRecorderProps {
  onAudioReady: (data: AudioData) => void;
}

export default function AudioRecorder({ onAudioReady }: AudioRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [stream, setStream] = useState<MediaStream | undefined>(undefined);
  const [recordedAudio, setRecordedAudio] = useState<AudioData | null>(null);
  const [duration, setDuration] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<NodeJS.Timeout | undefined>(undefined);
  const audioPlayerRef = useRef<HTMLAudioElement | null>(null);

  const startRecording = async () => {
    try {
      const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setStream(audioStream);

      const mediaRecorder = new MediaRecorder(audioStream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        const url = URL.createObjectURL(blob);
        const data = { blob, url, duration };
        setRecordedAudio(data);
        onAudioReady(data);

        // Stop all tracks
        audioStream.getTracks().forEach(track => track.stop());
        setStream(undefined);
      };

      mediaRecorder.start();
      setIsRecording(true);

      // Start timer
      setDuration(0);
      timerRef.current = setInterval(() => {
        setDuration(prev => prev + 1);
      }, 1000);

    } catch (err) {
      console.error("Error accessing microphone:", err);
      alert("الرجاء السماح بالوصول إلى الميكروفون للتسجيل");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      clearInterval(timerRef.current);
    }
  };

  const resetRecording = () => {
    setRecordedAudio(null);
    setDuration(0);
    setIsPlaying(false);
    if (audioPlayerRef.current) {
      audioPlayerRef.current.pause();
      audioPlayerRef.current.currentTime = 0;
    }
  };

  const togglePlayback = () => {
    if (!audioPlayerRef.current || !recordedAudio) return;

    if (isPlaying) {
      audioPlayerRef.current.pause();
      setIsPlaying(false);
    } else {
      audioPlayerRef.current.play();
      setIsPlaying(true);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const url = URL.createObjectURL(file);
      // Create a temporary audio element to get duration
      const audio = new Audio(url);
      audio.onloadedmetadata = () => {
        const data = { blob: file, url, duration: Math.floor(audio.duration) };
        setRecordedAudio(data);
        onAudioReady(data);
      };
    }
  };

  return (
    <div className="w-full max-w-md mx-auto bg-white p-6 rounded-2xl shadow-sm border border-stone-100 flex flex-col items-center gap-6">
      {!recordedAudio ? (
        <>
          <div className="h-32 w-full bg-stone-50 rounded-xl overflow-hidden flex items-center justify-center relative">
            {isRecording ? (
              <WaveformVisualizer stream={stream} color="#ef4444" />
            ) : (
              <div className="text-stone-400 text-sm">اضغط على الميكروفون للبدء</div>
            )}
            {isRecording && (
              <div className="absolute top-2 left-2 bg-red-100 text-red-600 px-2 py-1 rounded text-xs font-bold animate-pulse">
                تسجيل {formatTime(duration)}
              </div>
            )}
          </div>

          <div className="flex gap-4 items-center">
            {!isRecording ? (
              <button
                onClick={startRecording}
                className="w-16 h-16 rounded-full bg-stone-900 text-white flex items-center justify-center hover:bg-stone-800 transition-colors shadow-lg hover:scale-105 transform duration-200"
              >
                <Mic size={28} />
              </button>
            ) : (
              <button
                onClick={stopRecording}
                className="w-16 h-16 rounded-full bg-red-500 text-white flex items-center justify-center hover:bg-red-600 transition-colors shadow-lg animate-pulse"
              >
                <Square size={28} fill="currentColor" />
              </button>
            )}
          </div>

          <div className="relative">
            <input
              type="file"
              accept="audio/*"
              onChange={handleFileUpload}
              className="absolute inset-0 opacity-0 cursor-pointer w-full"
            />
            <button className="text-stone-500 text-sm flex items-center gap-2 hover:text-stone-800 transition-colors">
              <Upload size={16} />
              أو قم برفع ملف صوتي
            </button>
          </div>
        </>
      ) : (
        <>
          <div className="h-32 w-full bg-stone-900 rounded-xl flex items-center justify-center relative overflow-hidden">
            {/* Visualizer for playback could go here if we decode the blob */}
            <div className="w-full h-full flex items-center justify-center gap-1">
              {[...Array(20)].map((_, i) => (
                <div key={i} className="w-1 bg-stone-700 rounded-full" style={{ height: `${Math.random() * 60 + 20}%` }}></div>
              ))}
            </div>
          </div>

          <div className="w-full flex items-center justify-between">
            <button onClick={resetRecording} className="text-red-500 hover:bg-red-50 p-2 rounded-full transition-colors">
              <Trash2 size={20} />
            </button>

            <div className="flex flex-col items-center">
              <button
                onClick={togglePlayback}
                className="w-14 h-14 rounded-full bg-stone-900 text-white flex items-center justify-center hover:bg-stone-800 transition-colors shadow-md"
              >
                {isPlaying ? <Pause size={24} fill="currentColor" /> : <Play size={24} fill="currentColor" className="mr-1" />}
              </button>
              <span className="text-xs text-stone-500 mt-2 font-mono">
                {/* We would update this with current time */}
                {formatTime(recordedAudio.duration)}
              </span>
            </div>

            <div className="w-10"></div> {/* Spacer for balance */}
          </div>

          <audio
            ref={audioPlayerRef}
            src={recordedAudio.url}
            onEnded={() => setIsPlaying(false)}
            className="hidden"
          />
        </>
      )}
    </div>
  );
}
