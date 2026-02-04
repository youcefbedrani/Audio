import 'package:flutter/foundation.dart';
import 'package:just_audio/just_audio.dart';
import 'package:audio_session/audio_session.dart';

class AudioService {
  static final AudioService _instance = AudioService._internal();
  factory AudioService() => _instance;
  AudioService._internal();

  final AudioPlayer _audioPlayer = AudioPlayer();
  bool _isInitialized = false;

  Future<void> initialize() async {
    if (_isInitialized) return;

    try {
      final session = await AudioSession.instance;
      await session.configure(const AudioSessionConfiguration.music());
      _isInitialized = true;
    } catch (e) {
      print('Error initializing audio service: $e');
    }
  }

  Future<void> playAudio(String audioUrl) async {
    try {
      debugPrint('🎵 ===== AudioService.playAudio START =====');
      debugPrint('🎵 Audio URL received: $audioUrl');
      print('🎵 ===== AudioService.playAudio START =====');
      print('🎵 Audio URL received: $audioUrl');
      print('🎵 URL length: ${audioUrl.length}');
      
      // Validate URL - must be from Cloudinary or valid HTTP(S)
      if (audioUrl.isEmpty || audioUrl == 'null') {
        throw Exception('Audio URL is empty');
      }
      
      if (!audioUrl.startsWith('http://') && !audioUrl.startsWith('https://')) {
        throw Exception('Invalid audio URL format - must be HTTP/HTTPS: $audioUrl');
      }
      
      // Verify it's a Cloudinary URL (expected source)
      if (audioUrl.contains('cloudinary.com')) {
        print('✅ Audio URL is from Cloudinary: ${audioUrl.substring(0, 60)}...');
      } else {
        print('⚠️ Audio URL is not from Cloudinary: ${audioUrl.substring(0, 60)}...');
      }
      
      await initialize();
      print('🎵 Audio service initialized');
      
      // Stop any current playback
      try {
        await _audioPlayer.stop();
        print('🎵 Stopped previous audio');
      } catch (e) {
        print('⚠️ No previous audio to stop: $e');
      }
      
      print('🎵 Setting audio URL from Cloudinary...');
      print('🎵 Full URL: $audioUrl');
      
      // Set the audio URL - just_audio handles Cloudinary URLs directly
      await _audioPlayer.setUrl(audioUrl);
      print('✅ Audio URL loaded successfully into player');
      
      // Wait for audio to be ready
      await Future.delayed(const Duration(milliseconds: 300));
      
      print('🎵 Starting playback...');
      await _audioPlayer.play();
      print('✅ Play command sent');
      
      // Wait and verify playback
      await Future.delayed(const Duration(milliseconds: 1000));
      
      final state = _audioPlayer.playerState;
      final playing = _audioPlayer.playing;
      final duration = _audioPlayer.duration;
      
      print('🎵 ===== Audio Status =====');
      print('🎵 Player State: $state');
      print('🎵 Is Playing: $playing');
      print('🎵 Duration: $duration');
      print('🎵 Position: ${_audioPlayer.position}');
      
      if (!playing) {
        print('⚠️ Audio not playing yet, waiting...');
        await Future.delayed(const Duration(milliseconds: 1000));
        print('🎵 Now playing: ${_audioPlayer.playing}');
        
        if (!_audioPlayer.playing) {
          throw Exception('Audio failed to start playing. State: ${_audioPlayer.playerState}');
        }
      }
      
      print('✅ Audio is now playing!');
      print('🎵 ===== AudioService.playAudio SUCCESS =====');
      
    } catch (e, stackTrace) {
      print('❌ ===== AudioService ERROR =====');
      print('❌ Error: $e');
      print('❌ Stack trace: $stackTrace');
      print('❌ Audio URL was: $audioUrl');
      print('❌ Player state: ${_audioPlayer.playerState}');
      throw Exception('Failed to play audio: $e');
    }
  }

  Future<void> pauseAudio() async {
    try {
      await _audioPlayer.pause();
    } catch (e) {
      print('Error pausing audio: $e');
    }
  }

  Future<void> resumeAudio() async {
    try {
      await _audioPlayer.play();
    } catch (e) {
      print('Error resuming audio: $e');
    }
  }

  Future<void> stopAudio() async {
    try {
      await _audioPlayer.stop();
    } catch (e) {
      print('Error stopping audio: $e');
    }
  }

  Future<void> seekTo(Duration position) async {
    try {
      await _audioPlayer.seek(position);
    } catch (e) {
      print('Error seeking audio: $e');
    }
  }

  Stream<Duration> get positionStream => _audioPlayer.positionStream;
  Stream<Duration?> get durationStream => _audioPlayer.durationStream;
  Stream<PlayerState> get playerStateStream => _audioPlayer.playerStateStream;
  Stream<bool> get playingStream => _audioPlayer.playingStream;

  Duration get position => _audioPlayer.position;
  Duration? get duration => _audioPlayer.duration;
  PlayerState get playerState => _audioPlayer.playerState;
  bool get isPlaying => _audioPlayer.playing;

  Future<void> dispose() async {
    await _audioPlayer.dispose();
  }
}
