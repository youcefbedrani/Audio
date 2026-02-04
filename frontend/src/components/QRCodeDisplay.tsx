'use client';

import React from 'react';
import Image from 'next/image';
import QRCode from 'react-qr-code';
import { Download, Share2 } from 'lucide-react';

interface QRCodeDisplayProps {
  frameId: number;
  frameTitle: string;
  qrCodeUrl?: string;
  size?: number;
}

const QRCodeDisplay: React.FC<QRCodeDisplayProps> = ({
  frameId,
  frameTitle,
  qrCodeUrl,
  size = 200,
}) => {
  const qrValue = `audio_frame://frame/${frameId}`;

  const downloadQRCode = () => {
    const svg = document.getElementById('qr-code-svg');
    if (svg) {
      const svgData = new XMLSerializer().serializeToString(svg);
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new window.Image();
      
      canvas.width = size;
      canvas.height = size;
      
      img.onload = () => {
        ctx?.drawImage(img, 0, 0);
        const pngFile = canvas.toDataURL('image/png');
        
        const downloadLink = document.createElement('a');
        downloadLink.download = `qr-code-${frameTitle.replace(/\s+/g, '-').toLowerCase()}.png`;
        downloadLink.href = pngFile;
        downloadLink.click();
      };
      
      img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
    }
  };

  const shareQRCode = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: `QR Code for ${frameTitle}`,
          text: `Scan this QR code to listen to the audio message for ${frameTitle}`,
          url: qrValue,
        });
      } catch (error) {
        console.log('Error sharing:', error);
      }
    } else {
      // Fallback: copy to clipboard
      try {
        await navigator.clipboard.writeText(qrValue);
        alert('QR code URL copied to clipboard!');
      } catch (error) {
        console.log('Error copying to clipboard:', error);
      }
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <div className="text-center">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          QR Code for {frameTitle}
        </h3>
        
        {/* QR Code Display */}
        <div className="flex justify-center mb-6">
          <div className="bg-white p-4 rounded-lg border-2 border-gray-200">
            {qrCodeUrl ? (
              <Image
                src={qrCodeUrl}
                alt={`QR Code for ${frameTitle}`}
                width={size}
                height={size}
                className="rounded"
              />
            ) : (
              <QRCode
                id="qr-code-svg"
                value={qrValue}
                size={size}
                style={{ height: 'auto', maxWidth: '100%', width: '100%' }}
              />
            )}
          </div>
        </div>

        {/* QR Code Information */}
        <div className="mb-6">
          <p className="text-sm text-gray-600 mb-2">
            Scan this QR code with the Audio Art Frame mobile app to listen to the audio message.
          </p>
          <div className="bg-gray-50 rounded-lg p-3">
            <p className="text-xs text-gray-500 font-mono break-all">
              {qrValue}
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center space-x-4">
          <button
            onClick={downloadQRCode}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Download className="w-4 h-4" />
            <span>Download</span>
          </button>
          
          <button
            onClick={shareQRCode}
            className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <Share2 className="w-4 h-4" />
            <span>Share</span>
          </button>
        </div>

        {/* Instructions */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 className="text-sm font-semibold text-blue-900 mb-2">
            How to use:
          </h4>
          <ol className="text-sm text-blue-800 space-y-1 text-left">
            <li>1. Download the Audio Art Frame mobile app</li>
            <li>2. Open the app and tap &quot;Scan QR Code&quot;</li>
            <li>3. Point your camera at this QR code</li>
            <li>4. Listen to the audio message</li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default QRCodeDisplay;
