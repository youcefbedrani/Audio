import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/frame.dart';
import '../models/scan_response.dart';

class ApiService {
  // API URL - change to your computer's IP address for phone access
  // For local testing: http://localhost:8001/api
  // For phone access: http://YOUR_IP:8001/api (replace YOUR_IP with your computer's IP)
  // Current IP detected: 192.168.1.18
  // To find your IP: run 'hostname -I' or 'ip addr show'
  static const String baseUrl = 'http://10.0.2.2:8001/api';
  
  static Future<Map<String, String>> _getHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }

  /// Scan frame by frame ID (legacy method)
  static Future<ScanResponse> scanFrame(int frameId) async {
    return await _scanAudio(frameId, isOrderId: false);
  }
  
  /// Play audio by order ID or audio ID
  static Future<ScanResponse> playAudio(int audioOrOrderId) async {
    return await _scanAudio(audioOrOrderId, isOrderId: true);
  }
  
  /// Clean ID from QR code format
  static String cleanId(String raw) {
    return raw
        .replaceAll("audio_frame://play/", "")
        .replaceAll(RegExp(r'[^A-Za-z0-9]'), "")
        .toUpperCase()
        .trim();
  }
  
  /// Internal method to scan/play audio by ID
  static Future<ScanResponse> _scanAudio(int id, {required bool isOrderId}) async {
    try {
      // Use /api/audio/{id}/ endpoint for all scans
      String apiUrl = '$baseUrl/audio/$id/';
      print('🌐 Calling API: $apiUrl');
      print('   ID: $id');
      
      var response = await http.get(
        Uri.parse(apiUrl),
        headers: await _getHeaders(),
      ).timeout(
        const Duration(seconds: 10),
        onTimeout: () {
          throw Exception('Request timeout - server not responding');
        },
      );

      print('📡 Response status: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('✅ Received audio response');
        
        // Validate response has required fields
        if (data['audio_url'] == null || data['audio_url'] == '') {
          throw Exception('No audio URL in API response');
        }
        
        // Map response to ScanResponse format
        final audioUrl = data['signed_audio_url'] ?? data['audio_url'] ?? '';
        final waveformUrl = data['waveform_url'] ?? '';
        
        print('✅ Audio URL: ${audioUrl.isNotEmpty ? audioUrl.substring(0, 60) + "..." : "EMPTY"}');
        
        return ScanResponse.fromJson({
          'frame_id': data['frame_id'] ?? data['audio_id'] ?? id,
          'frame_title': data['frame_title'] ?? 'Audio',
          'audio_url': audioUrl,
          'signed_audio_url': audioUrl,
          'message': data['message'] ?? 'Audio found',
          'waveform_url': waveformUrl,
          'order_id': data['order_id'],
        });
      } else if (response.statusCode == 404) {
        throw Exception('Audio not found (404)');
      } else {
        throw Exception('Server error: ${response.statusCode}');
      }
    } on http.ClientException catch (e) {
      print('❌ Network error: $e');
      throw Exception('Network error: ${e.message}');
    } catch (e) {
      print('❌ Error in _scanAudio: $e');
      throw Exception('Error retrieving audio: $e');
    }
  }
  
  /// Scan frame by scan ID from QR code
  static Future<ScanResponse> scanByScanId(String scanId) async {
    try {
      final cleanedId = cleanId(scanId);
      print('🔍 Scanning with ID: $cleanedId (from raw: $scanId)');
      
      // Use /api/audio/{id}/ endpoint
      String apiUrl = '$baseUrl/audio/$cleanedId/';
      print('🌐 Calling API: $apiUrl');
      
      var response = await http.get(
        Uri.parse(apiUrl),
        headers: await _getHeaders(),
      ).timeout(
        const Duration(seconds: 10),
        onTimeout: () {
          throw Exception('Request timeout - server not responding');
        },
      );

      print('📡 Response status: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('✅ Received audio response');
        
        final audioUrl = data['signed_audio_url'] ?? data['audio_url'] ?? '';
        
        if (audioUrl.isEmpty) {
          throw Exception('No audio URL in response');
        }
        
        return ScanResponse.fromJson({
          'frame_id': data['frame_id'] ?? data['audio_id'],
          'frame_title': data['frame_title'] ?? 'Audio',
          'audio_url': audioUrl,
          'signed_audio_url': audioUrl,
          'message': data['message'] ?? 'Audio found',
          'waveform_url': data['waveform_url'] ?? '',
          'order_id': data['order_id'],
        });
      } else if (response.statusCode == 404) {
        throw Exception('Audio not found');
      } else {
        throw Exception('Server error: ${response.statusCode}');
      }
    } catch (e) {
      print('❌ Error scanning: $e');
      throw Exception('Failed to scan: $e');
    }
  }
  
  /// Fallback to legacy scan endpoint - DEPRECATED, kept for compatibility
  static Future<ScanResponse> _fallbackScanFrame(int frameId) async {
    print('🌐 Falling back to legacy scan endpoint: $baseUrl/scan/$frameId/');
    final response = await http.get(
      Uri.parse('$baseUrl/scan/$frameId/'),
      headers: await _getHeaders(),
    ).timeout(
      const Duration(seconds: 10),
      onTimeout: () {
        throw Exception('Request timeout - server not responding');
      },
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      print('✅ Received scan response: $data');
      
      // Ensure we have audio URL from Supabase/Cloudinary
      final audioUrl = data['signed_audio_url'] ?? data['audio_url'] ?? '';
      
      print('📥 Audio URL from API: ${audioUrl.isNotEmpty ? audioUrl.substring(0, 80) + "..." : "EMPTY"}');
      
      if (audioUrl.isEmpty) {
        throw Exception('No audio URL in response - order may not have audio file');
      }
      
      // Ensure waveform_url is included
      final scanResponse = ScanResponse.fromJson({
        ...data,
        'audio_url': audioUrl,
        'signed_audio_url': audioUrl,
        'waveform_url': data['waveform_url'] ?? '',
      });
      
      print('✅ ScanResponse created with audio URL from Cloudinary');
      return scanResponse;
    } else if (response.statusCode == 404) {
      throw Exception('Frame not found (404)');
    } else {
      throw Exception('Server error: ${response.statusCode}');
    }
  }


  static Future<PlayTrackResponse> trackPlay(int frameId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/track-play/$frameId/'),
        headers: await _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return PlayTrackResponse.fromJson(data);
      } else {
        throw Exception('Failed to track play: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error tracking play: $e');
    }
  }

  static Future<List<Frame>> getFrames() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/frames/'),
        headers: await _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> framesJson = data is List ? data : data['results'] ?? [];
        return framesJson.map((json) => Frame.fromJson(json)).toList();
      } else {
        throw Exception('Failed to load frames: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error loading frames: $e');
    }
  }

  static Future<Frame> getFrame(int frameId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/frames/$frameId/'),
        headers: await _getHeaders(),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return Frame.fromJson(data);
      } else {
        throw Exception('Failed to load frame: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error loading frame: $e');
    }
  }

  static Future<void> saveScanHistory(int frameId, String frameTitle) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final historyJson = prefs.getString('scan_history') ?? '[]';
      final List<dynamic> history = json.decode(historyJson);
      
      // Add new scan to history
      history.insert(0, {
        'frame_id': frameId,
        'frame_title': frameTitle,
        'scanned_at': DateTime.now().toIso8601String(),
      });
      
      // Keep only last 50 scans
      if (history.length > 50) {
        history.removeRange(50, history.length);
      }
      
      await prefs.setString('scan_history', json.encode(history));
    } catch (e) {
      print('Error saving scan history: $e');
    }
  }

  static Future<List<Map<String, dynamic>>> getScanHistory() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final historyJson = prefs.getString('scan_history') ?? '[]';
      final List<dynamic> history = json.decode(historyJson);
      return history.cast<Map<String, dynamic>>();
    } catch (e) {
      print('Error loading scan history: $e');
      return [];
    }
  }

  static Future<void> savePlayCount(int frameId) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final playCountsJson = prefs.getString('play_counts') ?? '{}';
      final Map<String, dynamic> playCounts = json.decode(playCountsJson);
      
      final currentCount = playCounts[frameId.toString()] ?? 0;
      playCounts[frameId.toString()] = currentCount + 1;
      
      await prefs.setString('play_counts', json.encode(playCounts));
    } catch (e) {
      print('Error saving play count: $e');
    }
  }

  static Future<int> getPlayCount(int frameId) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final playCountsJson = prefs.getString('play_counts') ?? '{}';
      final Map<String, dynamic> playCounts = json.decode(playCountsJson);
      return playCounts[frameId.toString()] ?? 0;
    } catch (e) {
      print('Error loading play count: $e');
      return 0;
    }
  }
}
