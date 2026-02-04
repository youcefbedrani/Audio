class ScanResponse {
  final int frameId;
  final String frameTitle;
  final String audioUrl;
  final String signedAudioUrl;
  final String message;
  final String? waveformUrl;
  final int? orderId;

  ScanResponse({
    required this.frameId,
    required this.frameTitle,
    required this.audioUrl,
    required this.signedAudioUrl,
    required this.message,
    this.waveformUrl,
    this.orderId,
  });

  factory ScanResponse.fromJson(Map<String, dynamic> json) {
    return ScanResponse(
      frameId: json['frame_id'] ?? json['audio_id'],
      frameTitle: json['frame_title'] ?? 'Audio',
      audioUrl: json['audio_url'] ?? '',
      signedAudioUrl: json['signed_audio_url'] ?? json['audio_url'] ?? '',
      message: json['message'] ?? 'Audio found',
      waveformUrl: json['waveform_url'],
      orderId: json['order_id'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'frame_id': frameId,
      'frame_title': frameTitle,
      'audio_url': audioUrl,
      'signed_audio_url': signedAudioUrl,
      'message': message,
      'waveform_url': waveformUrl,
      'order_id': orderId,
    };
  }
}

class PlayTrackResponse {
  final String message;
  final int playsCount;

  PlayTrackResponse({
    required this.message,
    required this.playsCount,
  });

  factory PlayTrackResponse.fromJson(Map<String, dynamic> json) {
    return PlayTrackResponse(
      message: json['message'],
      playsCount: json['plays_count'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'message': message,
      'plays_count': playsCount,
    };
  }
}
