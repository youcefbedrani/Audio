"use client";

import { useEffect, useState } from "react";
import Script from "next/script";
import { getSettings } from "@/lib/api";

declare global {
    interface Window {
        fbq: any;
        ttq: any;
        _fbq: any;
        pixelGlobalSettings: { fb: string; tt: string };
    }
}

export const trackEvent = (eventName: string, options?: any, userData?: any) => {
    if (typeof window === "undefined") return;

    // Facebook Pixel
    if (window.fbq) {
        // Advanced Matching: If user data is provided, re-init to send hash
        if (userData && window.pixelGlobalSettings?.fb) {
            try {
                const advancedMatchingParameters: any = {};

                // 1. Phone: Remove leading 0, add +213, remove spaces
                if (userData.phone) {
                    let ph = userData.phone.replace(/\D/g, ''); // keep only digits
                    if (ph.startsWith('0')) ph = ph.substring(1);
                    if (!ph.startsWith('213')) ph = '213' + ph;
                    advancedMatchingParameters.ph = ph;
                }

                // 2. Name: Split into fn/ln
                if (userData.name) {
                    const parts = userData.name.trim().split(" ");
                    if (parts.length > 0) advancedMatchingParameters.fn = parts[0].toLowerCase();
                    if (parts.length > 1) advancedMatchingParameters.ln = parts.slice(1).join(" ").toLowerCase();
                }

                // 3. Location
                if (userData.wilaya) advancedMatchingParameters.st = userData.wilaya.toLowerCase(); // State/Wilaya
                if (userData.address) advancedMatchingParameters.ct = userData.address.toLowerCase(); // City (approx)
                advancedMatchingParameters.country = 'dz';

                console.log("[PixelTracker] Sending Advanced Matching:", advancedMatchingParameters);
                window.fbq('init', window.pixelGlobalSettings.fb, advancedMatchingParameters);
            } catch (e) {
                console.error("[PixelTracker] Error processing user data", e);
            }
        }

        window.fbq("track", eventName, options);
    }

    // TikTok Pixel
    if (window.ttq) {
        window.ttq.track(eventName, options);
    }
};

export default function PixelTracker() {
    const [pixelIds, setPixelIds] = useState<{ fb: string; tt: string }>({ fb: "", tt: "" });

    useEffect(() => {
        const fetchPixels = async () => {
            try {
                const settings = await getSettings();
                // Sanitize IDs - ensure they are not "null" strings or falsy, and TRIM whitespace
                const fb = (settings.fb_pixel_id && settings.fb_pixel_id !== "null") ? settings.fb_pixel_id.trim() : "";
                const tt = (settings.tiktok_pixel_id && settings.tiktok_pixel_id !== "null") ? settings.tiktok_pixel_id.trim() : "";

                console.log("[PixelTracker] Resolved IDs:", { raw_fb: settings.fb_pixel_id, final_fb: fb });

                // Store globally for trackEvent usage
                if (typeof window !== 'undefined') {
                    window.pixelGlobalSettings = { fb, tt };
                }

                setPixelIds({ fb, tt });
            } catch (err) {
                console.error("Failed to load pixel settings:", err);
            }
        };
        fetchPixels();
    }, []);

    return (
        <>
            {/* Facebook Pixel */}
            {pixelIds.fb && (
                <>
                    <Script id="fb-pixel" strategy="afterInteractive">
                        {`
              !function(f,b,e,v,n,t,s)
              {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
              n.callMethod.apply(n,arguments):n.queue.push(arguments)};
              if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
              n.queue=[];t=b.createElement(e);t.async=!0;
              t.src=v;s=b.getElementsByTagName(e)[0];
              s.parentNode.insertBefore(t,s)}(window, document,'script',
              'https://connect.facebook.net/en_US/fbevents.js');
              fbq('init', '${pixelIds.fb}');
              fbq('track', 'PageView');
            `}
                    </Script>
                    <noscript>
                        <img
                            height="1"
                            width="1"
                            style={{ display: "none" }}
                            src={`https://www.facebook.com/tr?id=${pixelIds.fb}&ev=PageView&noscript=1`}
                            alt="fb-pixel"
                        />
                    </noscript>
                </>
            )}

            {/* TikTok Pixel */}
            {pixelIds.tt && (
                <Script id="tiktok-pixel" strategy="afterInteractive">
                    {`
            !function (w, d, t) {
              w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","trackBy","analytics","getAuthorizedID"],ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e},ttq.load=function(e,n){var t="https://analytics.tiktok.com/i18n/pixel/events.js";ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=t,ttq._t=ttq._t||+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};var o=document.createElement("script");o.type="text/javascript",o.async=!0,o.src=t+"?sdkid="+e+"&lib="+t;var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)};
              ttq.load('${pixelIds.tt}');
              ttq.page();
            }(window, document, 'ttq');
          `}
                </Script>
            )}
        </>
    );
}
