import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:just_audio/just_audio.dart';
import '../models/scan_response.dart';
import '../services/api_service.dart';
import '../services/audio_service.dart';

class AudioPlayerScreen extends StatefulWidget {
  final ScanResponse scanResponse;

  const AudioPlayerScreen({
    super.key,
    required this.scanResponse,
  });

  @override
  State<AudioPlayerScreen> createState() => _AudioPlayerScreenState();
}

class _AudioPlayerScreenState extends State<AudioPlayerScreen> {
  final AudioService _audioService = AudioService();
  bool _isPlaying = false;
  bool _isLoading = false;
  Duration _position = Duration.zero;
  Duration _duration = Duration.zero;
  int _localPlayCount = 0;

  @override
  void initState() {
    super.initState();
    _loadLocalPlayCount();
    _setupAudioListeners();
    // Auto-play audio immediately when screen loads (Spotify-style)
    _autoPlayAudio();
  }

  Future<void> _loadLocalPlayCount() async {
    final count = await ApiService.getPlayCount(widget.scanResponse.frameId);
    setState(() {
      _localPlayCount = count;
    });
  }

  void _setupAudioListeners() {
    _audioService.positionStream.listen((position) {
      setState(() {
        _position = position;
      });
    });

    _audioService.durationStream.listen((duration) {
      setState(() {
        _duration = duration ?? Duration.zero;
      });
    });

    _audioService.playingStream.listen((playing) {
      setState(() {
        _isPlaying = playing;
      });
    });

    _audioService.playerStateStream.listen((playerState) {
      if (playerState.processingState == ProcessingState.completed) {
        _onPlaybackCompleted();
      }
    });
  }

  Future<void> _autoPlayAudio() async {
    // Auto-play when screen loads (Spotify-style scanning)
    debugPrint('🎵 Auto-play audio requested');
    debugPrint('🎵 Audio URL: ${widget.scanResponse.signedAudioUrl}');
    print('🎵 Auto-play audio requested');
    print('🎵 Audio URL: ${widget.scanResponse.signedAudioUrl}');
    await Future.delayed(const Duration(milliseconds: 500)); // Small delay for smooth transition
    print('🎵 Starting auto-play...');
    await _playAudio();
  }

  Future<void> _playAudio() async {
    try {
      setState(() {
        _isLoading = true;
      });

      final audioUrl = widget.scanResponse.signedAudioUrl;
      print('🎵 ===== STARTING AUDIO PLAYBACK =====');
      print('🎵 Audio URL from Supabase/Cloudinary: ${audioUrl.substring(0, 80)}...');
      print('🎵 Audio URL length: ${audioUrl.length}');
      print('🎵 Frame ID: ${widget.scanResponse.frameId}');
      print('🎵 Order ID: ${widget.scanResponse.orderId ?? "N/A"}');
      
      // Validate audio URL exists
      if (audioUrl.isEmpty || audioUrl == '' || audioUrl == 'null') {
        throw Exception('Audio URL is empty - no audio file found in Supabase');
      }
      
      // Validate URL format (must be Cloudinary URL)
      if (!audioUrl.startsWith('http://') && !audioUrl.startsWith('https://')) {
        throw Exception('Invalid audio URL format: $audioUrl');
      }
      
      // Verify it's from Cloudinary
      if (audioUrl.contains('cloudinary.com')) {
        print('✅ Audio URL is from Cloudinary - ready to play');
      } else {
        print('⚠️ Audio URL is not from Cloudinary - may not work: $audioUrl');
      }
      
      print('🎵 Calling audio service to play Cloudinary audio...');
      await _audioService.playAudio(audioUrl);
      
      print('✅ Audio started playing successfully');
      
      // Track play event
      try {
        await ApiService.trackPlay(widget.scanResponse.frameId);
        await ApiService.savePlayCount(widget.scanResponse.frameId);
      } catch (e) {
        print('⚠️ Failed to track play: $e');
        // Don't fail playback if tracking fails
      }
      
      // Update local play count
      setState(() {
        _localPlayCount++;
      });
    } catch (e) {
      print('❌ Error playing audio: $e');
      String errorMessage = 'Failed to play audio';
      
      if (e.toString().contains('Failed host lookup') || 
          e.toString().contains('Connection refused')) {
        errorMessage = 'Cannot load audio file.\n\nPlease check your internet connection.';
      } else if (e.toString().contains('404')) {
        errorMessage = 'Audio file not found.\n\nThe audio may have been deleted.';
      } else {
        errorMessage = 'Error: ${e.toString()}';
      }
      
      _showErrorDialog(errorMessage);
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _pauseAudio() async {
    await _audioService.pauseAudio();
  }


  Future<void> _stopAudio() async {
    await _audioService.stopAudio();
  }

  void _onPlaybackCompleted() {
    setState(() {
      _isPlaying = false;
      _position = Duration.zero;
    });
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Error'),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  String _formatDuration(Duration duration) {
    String twoDigits(int n) => n.toString().padLeft(2, '0');
    final minutes = twoDigits(duration.inMinutes.remainder(60));
    final seconds = twoDigits(duration.inSeconds.remainder(60));
    return '$minutes:$seconds';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('Now Playing'),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.keyboard_arrow_down, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Spacer(flex: 2),
              
              // Waveform Artwork
              Container(
                width: double.infinity,
                aspectRatio: 1,
                decoration: BoxDecoration(
                  color: Colors.grey[100],
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.05),
                      blurRadius: 20,
                      offset: const Offset(0, 10),
                    ),
                  ],
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(24),
                  child: widget.scanResponse.waveformUrl != null
                      ? Image.network(
                          widget.scanResponse.waveformUrl!,
                          fit: BoxFit.contain, // Contain to show full waveform code
                          errorBuilder: (context, error, stackTrace) =>
                              const Icon(Icons.music_note, size: 80, color: Colors.grey),
                        )
                      : const Icon(Icons.music_note, size: 80, color: Colors.grey),
                ),
              ),
              
              const Spacer(flex: 3),
              
              // Title and Info
              Text(
                widget.scanResponse.frameTitle,
                style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  letterSpacing: -0.5,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Text(
                widget.scanResponse.message,
                style: TextStyle(
                  fontSize: 16,
                  color: Colors.grey[600],
                ),
                textAlign: TextAlign.center,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              
              const Spacer(flex: 3),
              
              // Progress Bar
              if (_duration.inSeconds > 0) ...[
                SliderTheme(
                  data: SliderTheme.of(context).copyWith(
                    trackHeight: 4,
                    thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 6),
                    overlayShape: const RoundSliderOverlayShape(overlayRadius: 14),
                    activeTrackColor: Colors.black,
                    inactiveTrackColor: Colors.grey[200],
                    thumbColor: Colors.black,
                  ),
                  child: Slider(
                    value: _position.inSeconds.toDouble(),
                    max: _duration.inSeconds.toDouble(),
                    onChanged: (value) {
                      _audioService.seekTo(Duration(seconds: value.toInt()));
                    },
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        _formatDuration(_position),
                        style: TextStyle(color: Colors.grey[600], fontSize: 12),
                      ),
                      Text(
                        _formatDuration(_duration),
                        style: TextStyle(color: Colors.grey[600], fontSize: 12),
                      ),
                    ],
                  ),
                ),
              ],
              
              const SizedBox(height: 32),
              
              // Controls
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Rewind
                  IconButton(
                    iconSize: 32,
                    icon: const Icon(Icons.replay_10_rounded),
                    color: Colors.grey[800],
                    onPressed: () {
                         final newPos = _position - const Duration(seconds: 10);
                         _audioService.seekTo(newPos.isNegative ? Duration.zero : newPos);
                    },
                  ),
                  const SizedBox(width: 32),
                  
                  // Play/Pause
                  Container(
                    width: 72,
                    height: 72,
                    decoration: BoxDecoration(
                      color: Colors.black,
                      shape: BoxShape.circle,
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.2),
                          blurRadius: 10,
                          offset: const Offset(0, 4),
                        ),
                      ],
                    ),
                    child: IconButton(
                      iconSize: 32,
                      icon: _isLoading
                          ? const CircularProgressIndicator(color: Colors.white, strokeWidth: 2)
                          : Icon(
                              _isPlaying ? Icons.pause_rounded : Icons.play_arrow_rounded,
                              color: Colors.white,
                            ),
                      onPressed: _isLoading ? null : (_isPlaying ? _pauseAudio : _playAudio),
                    ),
                  ),
                  
                  const SizedBox(width: 32),
                  
                  // Forward / Stop
                   IconButton(
                    iconSize: 32,
                    icon: const Icon(Icons.stop_rounded),
                    color: Colors.grey[800],
                     onPressed: _isPlaying || _position.inSeconds > 0 ? _stopAudio : null,
                  ),
                ],
              ),
              
              const Spacer(flex: 2),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _audioService.dispose();
    super.dispose();
  }
}
