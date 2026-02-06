
import Hero from "@/components/landing/Hero";
import RevealMoment from "@/components/landing/RevealMoment";
import HowItWorks from "@/components/landing/HowItWorks";
import MarketingAngles from "@/components/landing/MarketingAngles";
import UnifiedOrderForm from "@/components/UnifiedOrderForm";
import FAQ from "@/components/landing/FAQ";
import Footer from "@/components/landing/Footer";

export default function Home() {
  return (
    <main className="rtl text-right">
      <Hero />
      <RevealMoment />
      <HowItWorks />
      <MarketingAngles />
      <UnifiedOrderForm />
      <FAQ />
      <Footer />
    </main>
  );
}