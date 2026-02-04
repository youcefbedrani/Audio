'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface OrderData {
  orderId: string
  customerName: string
  firstName?: string
  lastName?: string
  phone: string
  email?: string
  address?: string
  city?: string
  wilaya?: string
  baladya?: string
  postalCode?: string
  frameTitle: string
  frameType?: string
  framePrice: string
  totalAmount?: string
  hasAudio: boolean
  audioRecorded?: boolean
  audioFileUrl?: string
  paymentMethod?: string
}

export default function ThankYouPage() {
  const [orderData, setOrderData] = useState<OrderData | null>(null)
  const [debugInfo, setDebugInfo] = useState<string>('Loading...')

  useEffect(() => {
    console.log('=== NEXT.JS THANK YOU PAGE - LOADING ===')
    console.log('Current URL:', typeof window !== 'undefined' ? window.location.href : 'SSR')
    
    setDebugInfo('Page loaded, checking sessionStorage...')
    
    // Function to process data
    function loadData() {
      // Try to get data - with retry mechanism
      let storedOrderData: string | null = null
      
      try {
        storedOrderData = sessionStorage.getItem('orderData')
        console.log('SessionStorage check:', storedOrderData ? 'DATA FOUND' : 'NO DATA')
        setDebugInfo(storedOrderData ? `Data found (${storedOrderData.length} chars)` : 'NO DATA in sessionStorage')
        
        if (storedOrderData) {
          console.log('Data length:', storedOrderData.length)
          console.log('Data preview:', storedOrderData.substring(0, 200))
          setDebugInfo(`Found data: ${storedOrderData.substring(0, 100)}...`)
        } else {
          setDebugInfo('No data found in sessionStorage. All keys: ' + JSON.stringify(Object.keys(sessionStorage)))
        }
      } catch (e) {
        console.error('Error accessing sessionStorage:', e)
        setDebugInfo('ERROR accessing sessionStorage: ' + (e as Error).message)
      }
      
      // If no data, wait a bit and try again (in case page loaded too fast)
      if (!storedOrderData) {
        console.log('⚠️ No data found, waiting 500ms and retrying...')
        setDebugInfo('No data found, retrying in 500ms...')
        setTimeout(() => {
          try {
            storedOrderData = sessionStorage.getItem('orderData')
            console.log('Retry result:', storedOrderData ? 'DATA FOUND' : 'STILL NO DATA')
    if (storedOrderData) {
              setDebugInfo('Data found on retry!')
              processOrderData(storedOrderData)
            } else {
              console.error('❌ Still no data after retry')
              const allKeys = Object.keys(sessionStorage)
              console.log('All sessionStorage keys:', allKeys)
              setDebugInfo(`Still no data. Keys in sessionStorage: ${allKeys.join(', ') || 'NONE'}`)
            }
          } catch (e) {
            console.error('Error in retry:', e)
            setDebugInfo('Error in retry: ' + (e as Error).message)
          }
        }, 500)
        return
      }
      
      processOrderData(storedOrderData)
    }
    
    // Run immediately if in browser
    if (typeof window !== 'undefined') {
      loadData()
    }
    
    function processOrderData(orderDataString: string) {
      try {
        // Validate JSON string before parsing
        if (!orderDataString || orderDataString.trim() === '') {
          console.error('❌ Empty or invalid orderDataString')
          setDebugInfo('❌ Empty data in sessionStorage')
          return
        }
        
        let parsed
        try {
          parsed = JSON.parse(orderDataString)
        } catch (parseErr) {
          console.error('❌ JSON Parse Error:', parseErr)
          console.error('Raw string length:', orderDataString.length)
          console.error('Raw string (first 500 chars):', orderDataString.substring(0, 500))
          setDebugInfo(`❌ Invalid JSON: ${(parseErr as Error).message}`)
          return
        }
        
        console.log('=== NEXT.JS THANK YOU PAGE - START ===')
        console.log('Raw sessionStorage data (first 500 chars):', orderDataString.substring(0, 500))
        console.log('Full raw data length:', orderDataString.length)
        console.log('Parsed order object:', parsed)
        console.log('All keys in order:', Object.keys(parsed))
        console.log('Full order object:', JSON.stringify(parsed, null, 2))
        console.log('Order ID from parsed:', parsed.orderId || parsed.id || parsed.supabase_id)
        console.log('Customer fields:', {
          firstName: parsed.firstName || parsed.first_name,
          lastName: parsed.lastName || parsed.last_name,
          customerName: parsed.customerName || parsed.customer_name,
          phone: parsed.phone || parsed.customer_phone
        })
        console.log('Audio fields:', {
          hasAudio: parsed.hasAudio,
          audioRecorded: parsed.audioRecorded,
          audioFileUrl: parsed.audioFileUrl || parsed.audio_file_url
        })
        
        // DEBUG: Check if data looks valid
        if (!parsed || typeof parsed !== 'object') {
          console.error('❌ Order object is null, undefined, or not an object!')
          return
        }
        
        // CRITICAL: Get firstName and lastName FIRST (guaranteed from form)
        const firstName = (parsed.firstName || parsed.first_name || '').toString().trim()
        const lastName = (parsed.lastName || parsed.last_name || '').toString().trim()
        let customerName = (parsed.customerName || parsed.customer_name || '').toString().trim()
        
        console.log('=== DATA EXTRACTION ===')
        console.log('Raw firstName:', firstName, 'type:', typeof firstName, 'length:', firstName.length)
        console.log('Raw lastName:', lastName, 'type:', typeof lastName, 'length:', lastName.length)
        console.log('Raw customerName:', customerName)
        
        // PRIORITY 1: ALWAYS reconstruct from firstName + lastName (MOST RELIABLE - from form)
        if (firstName || lastName) {
          // Check if they're actual values (not "undefined" string)
          if (firstName && lastName && firstName !== 'undefined' && lastName !== 'undefined' && firstName !== '' && lastName !== '') {
            customerName = (firstName + ' ' + lastName).trim()
            console.log('✅ Constructed from firstName + lastName:', customerName)
          } else if (firstName && firstName !== 'undefined' && firstName !== '') {
            customerName = firstName.trim()
            console.log('✅ Using firstName only:', customerName)
          } else if (lastName && lastName !== 'undefined' && lastName !== '') {
            customerName = lastName.trim()
            console.log('✅ Using lastName only:', customerName)
          }
        }
        
        // If customerName still has "undefined" or is empty, clean it
        if (customerName.includes('undefined') || customerName === '') {
          console.warn('⚠️ Customer name invalid, cleaning...')
          customerName = customerName.replace(/undefined/gi, '').replace(/\s{2,}/g, ' ').trim()
        }
        
        // Final validation
        if (!customerName || customerName === '' || customerName === 'undefined undefined') {
          console.warn('⚠️ Customer name still invalid after cleanup, using fallback')
          customerName = 'غير محدد'
        }
        
        // Get phone - prioritize saved phone field
        let phone = (parsed.phone || parsed.customer_phone || parsed.customerPhone || '').toString().trim()
        
        console.log('Raw phone field:', phone, 'type:', typeof phone, 'length:', phone.length)
        
        // Clean up phone - remove "undefined" strings
        phone = phone.replace(/undefined/gi, '').trim()
        
        if (!phone || phone === '' || phone === 'undefined') {
          console.warn('⚠️ Phone invalid, using fallback')
          phone = 'غير محدد'
        }
        
        // Get audio URL - check all possible field names
        const audioFileUrl = (parsed.audioFileUrl || 
                             parsed.audio_file_url || 
                             parsed.audio_url || 
                             '').toString().trim()
        
        console.log('=== AUDIO CHECK ===')
        console.log('audioFileUrl:', audioFileUrl)
        console.log('hasAudio:', parsed.hasAudio)
        console.log('audioRecorded:', parsed.audioRecorded)
        
        // Determine audio status - check multiple fields
        const hasAudio = !!(parsed.hasAudio || 
                           parsed.audioRecorded || 
                           audioFileUrl ||
                           parsed.audio_file_url || 
                           parsed.audio_file ||
                           parsed.audio_uploaded ||
                           parsed.has_audio)
        
        console.log('=== FINAL VALUES TO DISPLAY ===')
        console.log('Customer Name:', customerName)
        console.log('Phone:', phone)
        console.log('Audio URL:', audioFileUrl || 'N/A')
        console.log('Has Audio:', hasAudio)
        
        const normalized: OrderData = {
          orderId: parsed.orderId || parsed.id || parsed.supabase_id || 'N/A',
          firstName: firstName,
          lastName: lastName,
          customerName: customerName,
          phone: phone,
          email: parsed.email || parsed.customer_email || '',
          address: parsed.address || parsed.delivery_address || '',
          city: parsed.city || '',
          wilaya: parsed.wilaya || '',
          baladya: parsed.baladya || parsed.baladiya || '',
          postalCode: parsed.postalCode || parsed.postal_code || '',
          frameTitle: parsed.frameTitle || parsed.frame_title || parsed.frame?.title || 'غير محدد',
          frameType: parsed.frameType || parsed.frame_type || parsed.frame?.frame_type || '',
          framePrice: parsed.framePrice || parsed.frame_price || parsed.totalAmount || parsed.total_amount || parsed.frame?.price || '0',
          totalAmount: parsed.totalAmount || parsed.total_amount || '',
          paymentMethod: parsed.paymentMethod || parsed.payment_method || 'الدفع عند الاستلام',
          hasAudio: hasAudio,
          audioRecorded: hasAudio,
          audioFileUrl: audioFileUrl || undefined
        }
        
        console.log('✅ Setting normalized data:', {
          customerName: normalized.customerName,
          phone: normalized.phone,
          firstName: normalized.firstName,
          lastName: normalized.lastName,
          audioFileUrl: normalized.audioFileUrl || 'N/A',
          hasAudio: normalized.hasAudio
        })
        
        setDebugInfo(`✅ Data loaded successfully! Name: ${normalized.customerName}, Phone: ${normalized.phone}, Audio: ${normalized.hasAudio ? 'YES' : 'NO'}`)
        setOrderData(normalized)
      } catch (parseError) {
        console.error('❌ CRITICAL: Error parsing order data:', parseError)
        console.error('Raw data that failed to parse:', orderDataString)
        setDebugInfo(`❌ Parse Error: ${(parseError as Error).message}. Raw data: ${orderDataString.substring(0, 200)}`)
      }
    }
  }, [])

  if (!orderData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-2xl mx-auto px-4">
          <div className="text-6xl mb-4">❌</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">لا توجد بيانات طلب</h1>
          
          <Link href="/frames" className="text-blue-600 hover:text-blue-800">
            العودة للإطارات
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Link href="/" className="text-2xl font-bold text-blue-600">🎨 إطارات الصوت الفنية</Link>
            </div>
            <nav className="hidden md:flex space-x-reverse space-x-8">
              <Link href="/" className="text-gray-700 hover:text-blue-600">الرئيسية</Link>
              <Link href="/frames" className="text-gray-700 hover:text-blue-600">الإطارات</Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Success Message */}
        <div className="text-center mb-12">
          <div className="text-6xl mb-6">🎉</div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">شكراً لك على طلبك!</h1>
          <p className="text-xl text-gray-600 mb-2">تم استلام طلبك بنجاح وسنتواصل معك قريباً</p>
          {orderData && orderData.orderId && orderData.orderId !== 'N/A' && (
            <p className="text-sm text-green-600 font-semibold">✅ تم حفظ الطلب في قاعدة البيانات برقم: #{orderData.orderId}</p>
          )}
        </div>

        {/* Order Summary */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">📋 ملخص الطلب</h2>
          
          <div className="space-y-4">
            {/* Order ID */}
            <div className="flex justify-between items-center py-3 border-b border-gray-200">
              <span className="text-gray-600 font-medium">رقم الطلب:</span>
              <span className="font-bold text-blue-600 text-lg">#{orderData.orderId}</span>
            </div>
            
            {/* Customer Information Section */}
            <div className="mt-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">👤 معلومات العميل</h3>
              <div className="space-y-3 pl-4 border-r-4 border-blue-200">
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-600">الاسم الكامل:</span>
                  <span className="font-semibold text-gray-900">{orderData.customerName || `${orderData.firstName || ''} ${orderData.lastName || ''}`.trim() || 'غير محدد'}</span>
            </div>
            
                <div className="flex justify-between items-center py-2">
              <span className="text-gray-600">رقم الهاتف:</span>
              <span className="font-semibold text-gray-900">{orderData.phone}</span>
            </div>
            
                {orderData.email && (
                  <div className="flex justify-between items-center py-2">
                    <span className="text-gray-600">البريد الإلكتروني:</span>
                    <span className="font-semibold text-gray-900">{orderData.email}</span>
                  </div>
                )}
                
                {orderData.address && (
                  <div className="flex justify-between items-start py-2">
                    <span className="text-gray-600">العنوان:</span>
                    <span className="font-semibold text-gray-900 text-left max-w-xs">{orderData.address}</span>
                  </div>
                )}
                
                {(orderData.city || orderData.wilaya || orderData.baladya) && (
                  <div className="flex justify-between items-center py-2">
                    <span className="text-gray-600">الموقع:</span>
                    <span className="font-semibold text-gray-900">
                      {[orderData.baladya, orderData.wilaya, orderData.city].filter(Boolean).join('، ') || 'غير محدد'}
                    </span>
                  </div>
                )}
                
                {orderData.postalCode && (
                  <div className="flex justify-between items-center py-2">
                    <span className="text-gray-600">الرمز البريدي:</span>
                    <span className="font-semibold text-gray-900">{orderData.postalCode}</span>
                  </div>
                )}
              </div>
            </div>
            
            {/* Frame Information Section */}
            <div className="mt-6 pt-4 border-t border-gray-200">
              <h3 className="text-lg font-bold text-gray-900 mb-4">🖼️ معلومات الإطار</h3>
              <div className="space-y-3 pl-4 border-r-4 border-purple-200">
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-600">نوع الإطار:</span>
                  <span className="font-semibold text-gray-900">{orderData.frameTitle}</span>
                </div>
                
                {orderData.frameType && (
                  <div className="flex justify-between items-center py-2">
                    <span className="text-gray-600">المادة:</span>
                    <span className="font-semibold text-gray-900">{orderData.frameType}</span>
                  </div>
                )}
              </div>
            </div>
            
            {/* Pricing Section */}
            <div className="mt-6 pt-4 border-t border-gray-200">
              <h3 className="text-lg font-bold text-gray-900 mb-4">💰 المبلغ</h3>
              <div className="space-y-3 pl-4 border-r-4 border-green-200">
                <div className="flex justify-between items-center py-2">
                  <span className="text-gray-600">سعر الإطار:</span>
                  <span className="font-semibold text-gray-900">{orderData.framePrice} دج</span>
                </div>
                
                {orderData.totalAmount && orderData.totalAmount !== orderData.framePrice && (
                  <div className="flex justify-between items-center py-2">
                    <span className="text-gray-600">المبلغ الإجمالي:</span>
                    <span className="font-bold text-green-600 text-lg">{orderData.totalAmount} دج</span>
                  </div>
                )}
                
                <div className="flex justify-between items-center py-2 border-t border-gray-200 mt-3 pt-3">
              <span className="text-gray-600">طريقة الدفع:</span>
                  <span className="font-semibold text-gray-900">{orderData.paymentMethod || 'الدفع عند الاستلام'}</span>
                </div>
              </div>
            </div>
            
            {/* Audio Recording Section */}
            <div className="mt-6 pt-4 border-t border-gray-200">
              <h3 className="text-lg font-bold text-gray-900 mb-4">🎤 التسجيل الصوتي</h3>
              <div className={`p-4 rounded-lg ${orderData.hasAudio || orderData.audioRecorded ? 'bg-green-50 border-2 border-green-200' : 'bg-gray-50 border-2 border-gray-200'}`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    {orderData.hasAudio || orderData.audioRecorded ? (
                      <>
                        <span className="text-3xl mr-3">✅</span>
                        <div className="flex-1">
                          <span className="font-bold text-green-700 text-lg">تم تسجيل الرسالة الصوتية بنجاح!</span>
                          <p className="text-sm text-green-600 mt-1">سيتم ربط الرسالة الصوتية بالإطار ويمكنك الاستماع إليها عبر التطبيق</p>
                          {orderData.audioFileUrl && (
                            <div className="mt-3 p-2 bg-white rounded border border-green-300">
                              <p className="text-xs text-gray-600 mb-1">رابط الملف الصوتي:</p>
                              <a 
                                href={orderData.audioFileUrl} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-xs text-blue-600 hover:text-blue-800 break-all"
                              >
                                {orderData.audioFileUrl}
                              </a>
                            </div>
                          )}
                        </div>
                      </>
                    ) : (
                      <>
                        <span className="text-3xl mr-3">ℹ️</span>
                        <div>
                          <span className="font-semibold text-gray-600">لم يتم تسجيل رسالة صوتية</span>
                          <p className="text-sm text-gray-500 mt-1">يمكنك إضافة رسالة صوتية لاحقاً عبر التطبيق</p>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Next Steps */}
        <div className="bg-blue-50 rounded-lg p-8 mb-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">الخطوات التالية</h3>
          <div className="space-y-4">
            <div className="flex items-start">
              <div className="bg-blue-100 w-8 h-8 rounded-full flex items-center justify-center mr-3 mt-1">
                <span className="text-blue-600 font-bold text-sm">1</span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900">تأكيد الطلب</h4>
                <p className="text-gray-600">سنتواصل معك خلال 24 ساعة لتأكيد الطلب وتفاصيل التوصيل</p>
              </div>
            </div>
            
            <div className="flex items-start">
              <div className="bg-blue-100 w-8 h-8 rounded-full flex items-center justify-center mr-3 mt-1">
                <span className="text-blue-600 font-bold text-sm">2</span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900">إعداد الإطار</h4>
                <p className="text-gray-600">سنقوم بإعداد إطارك الفني مع رمز QR فريد خلال 3-5 أيام عمل</p>
              </div>
            </div>
            
            <div className="flex items-start">
              <div className="bg-blue-100 w-8 h-8 rounded-full flex items-center justify-center mr-3 mt-1">
                <span className="text-blue-600 font-bold text-sm">3</span>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900">التوصيل</h4>
                <p className="text-gray-600">سيتم توصيل إطارك إلى العنوان المحدد مع الدفع عند الاستلام</p>
              </div>
            </div>
          </div>
        </div>

        {/* App Download */}
        <div className="bg-green-50 rounded-lg p-8 mb-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">تحميل التطبيق</h3>
          <p className="text-gray-600 mb-6">
            لاستخدام إطارك الفني، ستحتاج إلى تحميل تطبيقنا المحمول لمسح رمز QR والاستماع للرسائل الصوتية
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4">
            <a 
              href="#" 
              className="flex items-center justify-center px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
            >
              <svg className="w-6 h-6 mr-2" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3.609 1.814L13.792 12L3.609 22.186a.996.996 0 01-.609-.92V2.734a1 1 0 01.609-.92zm10.89 10.893l2.302 2.302-10.937 6.333 8.635-8.635zm3.199-3.198l2.807 1.626a1 1 0 010 1.73l-2.808 1.626L13.5 12l4.198-2.491zM5.864 2.658L16.802 8.99l-3.75 3.75-7.188-7.188z"/>
              </svg>
              تحميل من Google Play
            </a>
            
            <a 
              href="#" 
              className="flex items-center justify-center px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors"
            >
              <svg className="w-6 h-6 mr-2" viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
              </svg>
              تحميل من App Store
            </a>
          </div>
        </div>

        {/* Tips */}
        <div className="bg-yellow-50 rounded-lg p-8 mb-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">نصائح للاستخدام</h3>
          <div className="space-y-3">
            <div className="flex items-start">
              <div className="text-yellow-600 mr-3 mt-1">💡</div>
              <p className="text-gray-700">احتفظ برقم الطلب للرجوع إليه عند الحاجة</p>
            </div>
            <div className="flex items-start">
              <div className="text-yellow-600 mr-3 mt-1">📱</div>
              <p className="text-gray-700">تأكد من تحميل التطبيق قبل استلام الإطار</p>
            </div>
            <div className="flex items-start">
              <div className="text-yellow-600 mr-3 mt-1">🎵</div>
              <p className="text-gray-700">يمكنك إضافة المزيد من الرسائل الصوتية لاحقاً عبر التطبيق</p>
            </div>
            <div className="flex items-start">
              <div className="text-yellow-600 mr-3 mt-1">📞</div>
              <p className="text-gray-700">لأي استفسارات، تواصل معنا على: 0555-123-456</p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="text-center space-y-4">
          <Link 
            href="/frames" 
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors font-semibold"
          >
            تصفح المزيد من الإطارات
          </Link>
          
          <div>
            <Link 
              href="/" 
              className="text-gray-600 hover:text-gray-800"
            >
              العودة للصفحة الرئيسية
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center mb-4">
              <div className="text-2xl font-bold">🎨 إطارات الصوت الفنية</div>
            </div>
            <p className="text-gray-400 mb-4">نجمع الفن والصوت معاً لتجارب لا تُنسى</p>
            <div className="flex justify-center space-x-reverse space-x-6">
              <Link href="/" className="text-gray-400 hover:text-white">الرئيسية</Link>
              <Link href="/frames" className="text-gray-400 hover:text-white">الإطارات</Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
