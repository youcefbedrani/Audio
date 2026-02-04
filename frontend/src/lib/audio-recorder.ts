/**
 * Audio recording utilities using MediaRecorder API
 */

export interface AudioRecorderOptions {
  mimeType?: string;
  audioBitsPerSecond?: number;
}

export class AudioRecorder {
  private mediaRecorder: MediaRecorder | null = null;
  private audioChunks: Blob[] = [];
  private stream: MediaStream | null = null;

  async startRecording(options: AudioRecorderOptions = {}): Promise<void> {
    try {
      // Get user media
      this.stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100,
        } 
      });

      // Check for supported MIME types
      const mimeTypes = [
        'audio/webm;codecs=opus',
        'audio/webm',
        'audio/mp4',
        'audio/wav',
        'audio/ogg;codecs=opus',
      ];

      let selectedMimeType = options.mimeType;
      if (!selectedMimeType) {
        selectedMimeType = mimeTypes.find(type => MediaRecorder.isTypeSupported(type)) || '';
      }

      // Create MediaRecorder
      this.mediaRecorder = new MediaRecorder(this.stream, {
        mimeType: selectedMimeType,
        audioBitsPerSecond: options.audioBitsPerSecond || 128000,
      });

      // Reset chunks
      this.audioChunks = [];

      // Handle data available
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };

      // Start recording
      this.mediaRecorder.start(1000); // Collect data every second
    } catch (error) {
      throw new Error(`Failed to start recording: ${error}`);
    }
  }

  stopRecording(): Promise<Blob> {
    return new Promise((resolve, reject) => {
      if (!this.mediaRecorder) {
        reject(new Error('No active recording'));
        return;
      }

      this.mediaRecorder.onstop = () => {
        const audioBlob = new Blob(this.audioChunks, { 
          type: this.mediaRecorder?.mimeType || 'audio/webm' 
        });
        resolve(audioBlob);
      };

      this.mediaRecorder.stop();
      this.cleanup();
    });
  }

  pauseRecording(): void {
    if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
      this.mediaRecorder.pause();
    }
  }

  resumeRecording(): void {
    if (this.mediaRecorder && this.mediaRecorder.state === 'paused') {
      this.mediaRecorder.resume();
    }
  }

  getRecordingState(): string | null {
    return this.mediaRecorder?.state || null;
  }

  isRecording(): boolean {
    return this.mediaRecorder?.state === 'recording';
  }

  isPaused(): boolean {
    return this.mediaRecorder?.state === 'paused';
  }

  private cleanup(): void {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }
    this.mediaRecorder = null;
  }

  // Static method to check if recording is supported
  static isSupported(): boolean {
    return !!(navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function' && typeof window.MediaRecorder !== 'undefined');
  }

  // Static method to get supported MIME types
  static getSupportedMimeTypes(): string[] {
    const mimeTypes = [
      'audio/webm;codecs=opus',
      'audio/webm',
      'audio/mp4',
      'audio/wav',
      'audio/ogg;codecs=opus',
    ];

    return mimeTypes.filter(type => MediaRecorder.isTypeSupported(type));
  }
}

// Utility function to create audio URL from blob
export const createAudioURL = (blob: Blob): string => {
  return URL.createObjectURL(blob);
};

// Utility function to revoke audio URL
export const revokeAudioURL = (url: string): void => {
  URL.revokeObjectURL(url);
};

// Utility function to get audio duration
export const getAudioDuration = (blob: Blob): Promise<number> => {
  return new Promise((resolve, reject) => {
    const audio = new Audio();
    const url = createAudioURL(blob);
    
    audio.addEventListener('loadedmetadata', () => {
      revokeAudioURL(url);
      resolve(audio.duration);
    });
    
    audio.addEventListener('error', () => {
      revokeAudioURL(url);
      reject(new Error('Failed to load audio'));
    });
    
    audio.src = url;
  });
};

// Utility function to format duration
export const formatDuration = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
};
