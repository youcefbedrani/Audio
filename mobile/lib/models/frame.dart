class Frame {
  final int id;
  final String title;
  final String description;
  final String frameType;
  final String image;
  final String? qrCode;
  final String? audioFile;
  final FrameOwner owner;
  final double price;
  final bool isAvailable;
  final DateTime createdAt;
  final DateTime updatedAt;
  final FrameStatistics statistics;

  Frame({
    required this.id,
    required this.title,
    required this.description,
    required this.frameType,
    required this.image,
    this.qrCode,
    this.audioFile,
    required this.owner,
    required this.price,
    required this.isAvailable,
    required this.createdAt,
    required this.updatedAt,
    required this.statistics,
  });

  factory Frame.fromJson(Map<String, dynamic> json) {
    return Frame(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      frameType: json['frame_type'],
      image: json['image'],
      qrCode: json['qr_code'],
      audioFile: json['audio_file'],
      owner: FrameOwner.fromJson(json['owner']),
      price: (json['price'] as num).toDouble(),
      isAvailable: json['is_available'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      statistics: FrameStatistics.fromJson(json['statistics']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'frame_type': frameType,
      'image': image,
      'qr_code': qrCode,
      'audio_file': audioFile,
      'owner': owner.toJson(),
      'price': price,
      'is_available': isAvailable,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'statistics': statistics.toJson(),
    };
  }
}

class FrameOwner {
  final int id;
  final String username;
  final String email;

  FrameOwner({
    required this.id,
    required this.username,
    required this.email,
  });

  factory FrameOwner.fromJson(Map<String, dynamic> json) {
    return FrameOwner(
      id: json['id'],
      username: json['username'],
      email: json['email'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
    };
  }
}

class FrameStatistics {
  final int scansCount;
  final int playsCount;
  final DateTime? lastScan;
  final DateTime? lastPlay;

  FrameStatistics({
    required this.scansCount,
    required this.playsCount,
    this.lastScan,
    this.lastPlay,
  });

  factory FrameStatistics.fromJson(Map<String, dynamic> json) {
    return FrameStatistics(
      scansCount: json['scans_count'],
      playsCount: json['plays_count'],
      lastScan: json['last_scan'] != null ? DateTime.parse(json['last_scan']) : null,
      lastPlay: json['last_play'] != null ? DateTime.parse(json['last_play']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'scans_count': scansCount,
      'plays_count': playsCount,
      'last_scan': lastScan?.toIso8601String(),
      'last_play': lastPlay?.toIso8601String(),
    };
  }
}
