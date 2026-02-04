'use client';

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
// import { Frame } from '@/lib/api'; // Removed broken import
import { Eye, Play, Scan } from 'lucide-react';

export interface Frame {
  id: number;
  title: string;
  description: string;
  price: number;
  image: string;
  frame_type: string;
  is_available: boolean;
  statistics?: {
    scans_count: number;
    plays_count: number;
  };
  audio_file?: string;
}

interface FrameCardProps {
  frame: Frame;
  showStats?: boolean;
}

const FrameCard: React.FC<FrameCardProps> = ({ frame, showStats = false }) => {
  const frameTypeLabels: { [key: string]: string } = {
    'wooden': 'خشبي',
    'metal': 'معدني',
    'plastic': 'بلاستيكي',
    'glass': 'زجاجي'
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      {/* Frame Image */}
      <div className="relative h-48 w-full">
        <Image
          src={frame.image || '/placeholder-frame.jpg'}
          alt={frame.title}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />

        {/* Frame Type Badge */}
        <div className="absolute top-2 right-2">
          <span className="bg-white/90 backdrop-blur-sm px-2 py-1 rounded-full text-xs font-medium text-gray-700">
            {frameTypeLabels[frame.frame_type] || frame.frame_type}
          </span>
        </div>

        {/* Price Badge */}
        <div className="absolute top-2 left-2">
          <span className="bg-green-600 text-white px-2 py-1 rounded-full text-sm font-semibold">
            {frame.price} دج
          </span>
        </div>
      </div>

      {/* Frame Details */}
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2 text-right">
          {frame.title}
        </h3>

        <p className="text-gray-600 text-sm mb-3 line-clamp-2 text-right">
          {frame.description}
        </p>

        {/* Statistics */}
        {showStats && (
          <div className="flex items-center justify-between mb-4 text-sm text-gray-500">
            <div className="flex items-center space-x-reverse space-x-1">
              <Scan className="w-4 h-4" />
              <span>{frame.statistics?.scans_count || 0} مسح</span>
            </div>
            <div className="flex items-center space-x-reverse space-x-1">
              <Play className="w-4 h-4" />
              <span>{frame.statistics?.plays_count || 0} تشغيل</span>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-reverse space-x-2">
          <Link
            href={`/frames/${frame.id}`}
            className="flex-1 flex items-center justify-center space-x-reverse space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Eye className="w-4 h-4" />
            <span>عرض التفاصيل</span>
          </Link>

          {frame.audio_file && (
            <button
              onClick={() => {
                // This would trigger audio playback in a modal or new page
                console.log('Play audio for frame:', frame.id);
              }}
              className="flex items-center justify-center space-x-reverse space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Play className="w-4 h-4" />
              <span>تشغيل</span>
            </button>
          )}
        </div>

        {/* Availability Status */}
        <div className="mt-3 text-center">
          {frame.is_available ? (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              متوفر
            </span>
          ) : (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
              غير متوفر
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default FrameCard;
