import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Check, X, Lightning, Crown, Rocket, Star, ArrowLeft, CurrencyDollar } from "@phosphor-icons/react";
import { useAuth, ThemeToggle } from "./AuthContext";
import { API } from "./constants";
import axios from "axios";
import { toast } from "sonner";

const PricingPage = () => {
  const { user, token, isDark } = useAuth();
  const d = isDark;
  const navigate = useNavigate();
  const [plans, setPlans] = useState([]);
  const [mySub, setMySub] = useState(null);
  const [currency, setCurrency] = useState("USD");
  const [loading, setLoading] = useState(true);
  const [activating, setActivating] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const [plansRes, subRes] = await Promise.all([
          axios.get(`${API}/subscription/plans`),
          token ? axios.get(`${API}/subscription/me`, { headers: { Authorization: `Bearer ${token}` } }) : null,
        ]);
        setPlans(plansRes.data.plans || []);
        if (subRes) setMySub(subRes.data);
      } catch (e) { console.error(e); }
      finally { setLoading(false); }
    };
    load();
  }, [token]);

  const handleSubscribe = async (planId) => {
    if (!token) {
      toast.error("Please sign in first");
      navigate("/");
      return;
    }
    if (planId === "free") {
      toast.info("You are already on the Free plan");
      return;
    }

    // For now, show coming soon for paid plans (ABA PayWay integration pending)
    setActivating(planId);
    try {
      // TODO: Replace with ABA PayWay checkout when keys are ready
      toast.info("ABA PayWay payment coming soon! Contact us to activate your plan.");
    } catch (e) {
      toast.error("Payment failed");
    } finally {
      setActivating(null);
    }
  };

  const planIcons = { free: Star, basic: Lightning, pro: Crown, business: Rocket };
  const planColors = {
    free: { gradient: "from-zinc-500 to-zinc-600", bg: d ? "bg-zinc-800/60" : "bg-white", border: d ? "border-zinc-700/50" : "border-zinc-200" },
    basic: { gradient: "from-sky-500 to-blue-600", bg: d ? "bg-zinc-800/60" : "bg-white", border: d ? "border-sky-500/20" : "border-sky-200" },
    pro: { gradient: "from-violet-500 to-purple-600", bg: d ? "bg-violet-950/30" : "bg-violet-50/50", border: d ? "border-violet-500/30" : "border-violet-300" },
    business: { gradient: "from-amber-500 to-orange-600", bg: d ? "bg-zinc-800/60" : "bg-white", border: d ? "border-amber-500/20" : "border-amber-200" },
  };

  const currentPlan = mySub?.subscription?.plan || "free";

  return (
    <div className={`min-h-screen ${d ? 'bg-zinc-950' : 'bg-zinc-50'}`} style={{ fontFamily: "'IBM Plex Sans', sans-serif" }}>
      {/* Header */}
      <header className={`sticky top-0 z-50 backdrop-blur-xl border-b ${d ? 'bg-zinc-950/90 border-zinc-800/50' : 'bg-white/90 border-zinc-200'}`}>
        <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={() => navigate(token ? "/dashboard" : "/")} className="flex items-center gap-2 transition-opacity hover:opacity-80">
              <img src="/voxidub-logo.png" alt="VoxiDub.AI" className="h-10 w-10 rounded-full object-cover border-2 border-zinc-200" />
              <span className={`text-lg font-bold tracking-tight ${d ? 'text-white' : 'text-zinc-950'}`} style={{ fontFamily: "'Outfit', sans-serif" }}>VoxiDub.AI</span>
            </button>
            <span className={`text-[9px] px-2.5 py-1 rounded-md font-bold tracking-[0.15em] uppercase ${d ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' : 'bg-amber-100 text-amber-700 border border-amber-200'}`}>Pricing</span>
          </div>
          <div className="flex items-center gap-3">
            {/* Currency toggle */}
            <div className={`flex items-center rounded-lg overflow-hidden border ${d ? 'border-zinc-700' : 'border-zinc-300'}`}>
              <button onClick={() => setCurrency("USD")} data-testid="currency-usd"
                className={`px-3 py-1.5 text-xs font-bold transition-all ${currency === "USD" ? (d ? 'bg-white text-zinc-900' : 'bg-zinc-900 text-white') : (d ? 'bg-zinc-800 text-zinc-400' : 'bg-white text-zinc-500')}`}>
                USD $
              </button>
              <button onClick={() => setCurrency("KHR")} data-testid="currency-khr"
                className={`px-3 py-1.5 text-xs font-bold transition-all ${currency === "KHR" ? (d ? 'bg-white text-zinc-900' : 'bg-zinc-900 text-white') : (d ? 'bg-zinc-800 text-zinc-400' : 'bg-white text-zinc-500')}`}>
                KHR
              </button>
            </div>
            <ThemeToggle />
            <button onClick={() => navigate(token ? "/dashboard" : "/")} className={`text-xs px-4 py-2 rounded-lg font-medium transition-all flex items-center gap-1.5 ${d ? 'bg-zinc-800 text-zinc-300 hover:bg-zinc-700' : 'bg-zinc-100 text-zinc-700 hover:bg-zinc-200'}`}>
              <ArrowLeft className="w-3 h-3" />{token ? "Dashboard" : "Home"}
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Title */}
        <div className="text-center mb-12">
          <h1 className={`text-3xl md:text-5xl font-light tracking-tighter ${d ? 'text-white' : 'text-zinc-900'}`} style={{ fontFamily: "'Outfit', sans-serif" }}>
            Choose Your <span className={`font-semibold ${d ? 'text-violet-400' : 'text-violet-600'}`}>Plan</span>
          </h1>
          <p className={`text-sm mt-3 max-w-md mx-auto ${d ? 'text-zinc-500' : 'text-zinc-500'}`}>
            AI-powered video dubbing. Any language to any language. Pay with ABA Pay, KHQR, Visa, or MasterCard.
          </p>
        </div>

        {/* Plans Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 max-w-6xl mx-auto">
          {plans.map((plan, i) => {
            const color = planColors[plan.id] || planColors.free;
            const Icon = planIcons[plan.id] || Star;
            const isPopular = plan.id === "pro";
            const isCurrent = currentPlan === plan.id;
            const price = currency === "USD" ? plan.price_usd : plan.price_khr;
            const priceLabel = currency === "USD" ? `$${price}` : `${price.toLocaleString()}`;
            const currLabel = currency === "USD" ? "/month" : "KHR/month";

            return (
              <motion.div key={plan.id}
                initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.08, duration: 0.5 }}
                data-testid={`plan-card-${plan.id}`}
                className={`relative rounded-2xl border p-6 flex flex-col transition-all duration-300
                  ${isPopular ? `ring-2 ${d ? 'ring-violet-500/50' : 'ring-violet-400'}` : ''}
                  ${color.bg} ${color.border}
                  ${d ? 'hover:border-zinc-500' : 'hover:shadow-xl hover:shadow-zinc-200/40'}`}
              >
                {/* Popular badge */}
                {isPopular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <span className="px-4 py-1 rounded-full text-[10px] font-bold tracking-[0.15em] uppercase bg-gradient-to-r from-violet-500 to-purple-600 text-white shadow-lg shadow-violet-500/30">
                      Most Popular
                    </span>
                  </div>
                )}

                {/* Current badge */}
                {isCurrent && (
                  <div className="absolute -top-3 right-4">
                    <span className={`px-3 py-1 rounded-full text-[10px] font-bold tracking-[0.12em] uppercase ${d ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-emerald-100 text-emerald-700 border border-emerald-300'}`}>
                      Current
                    </span>
                  </div>
                )}

                {/* Icon + Name */}
                <div className="flex items-center gap-3 mb-4 mt-1">
                  <div className={`w-11 h-11 rounded-xl flex items-center justify-center shadow-lg bg-gradient-to-br ${color.gradient}`}>
                    <Icon className="w-5 h-5 text-white" weight="fill" />
                  </div>
                  <div>
                    <div className={`text-lg font-semibold tracking-tight ${d ? 'text-white' : 'text-zinc-900'}`} style={{ fontFamily: "'Outfit', sans-serif" }}>{plan.name}</div>
                  </div>
                </div>

                {/* Price */}
                <div className="mb-5">
                  <div className="flex items-end gap-1">
                    <span className={`text-3xl font-bold tracking-tight ${d ? 'text-white' : 'text-zinc-900'}`}>{plan.price_usd === 0 ? "Free" : priceLabel}</span>
                    {plan.price_usd > 0 && <span className={`text-xs mb-1 ${d ? 'text-zinc-500' : 'text-zinc-400'}`}>{currLabel}</span>}
                  </div>
                </div>

                {/* Features */}
                <div className="flex-1 space-y-3 mb-6">
                  <Feature d={d} ok={true} text={plan.videos_per_month === -1 ? "Unlimited videos" : `${plan.videos_per_month} video${plan.videos_per_month > 1 ? 's' : ''}/month`} />
                  <Feature d={d} ok={true} text={`Max ${plan.max_duration_min} min per video`} />
                  <Feature d={d} ok={!plan.watermark} text={plan.watermark ? "Watermark on video" : "No watermark"} />
                  <Feature d={d} ok={plan.priority_queue} text={plan.priority_queue ? "Priority queue" : "Standard queue"} />
                  <Feature d={d} ok={true} text="Telegram delivery" />
                  <Feature d={d} ok={true} text="322+ AI voices" />
                  <Feature d={d} ok={plan.id !== "free"} text={plan.id !== "free" ? "All 9 tools" : "Limited tools"} />
                </div>

                {/* Button */}
                {isCurrent ? (
                  <button disabled className={`w-full py-3 rounded-xl text-sm font-bold transition-all ${d ? 'bg-zinc-700 text-zinc-400' : 'bg-zinc-200 text-zinc-500'}`} data-testid={`plan-btn-${plan.id}`}>
                    Current Plan
                  </button>
                ) : (
                  <button onClick={() => handleSubscribe(plan.id)} disabled={activating === plan.id}
                    data-testid={`plan-btn-${plan.id}`}
                    className={`w-full py-3 rounded-xl text-sm font-bold transition-all duration-200 active:scale-[0.98] shadow-lg
                      ${isPopular
                        ? 'bg-gradient-to-r from-violet-500 to-purple-600 text-white hover:shadow-xl hover:shadow-violet-500/30'
                        : plan.id === "free"
                          ? (d ? 'bg-zinc-700 text-white hover:bg-zinc-600' : 'bg-zinc-200 text-zinc-700 hover:bg-zinc-300')
                          : (d ? 'bg-white text-zinc-900 hover:bg-zinc-100' : `bg-gradient-to-r ${color.gradient} text-white hover:shadow-xl`)
                      }`}>
                    {activating === plan.id ? "Processing..." : plan.price_usd === 0 ? "Get Started" : "Subscribe"}
                  </button>
                )}
              </motion.div>
            );
          })}
        </div>

        {/* Payment methods */}
        <div className="mt-12 text-center">
          <p className={`text-xs ${d ? 'text-zinc-600' : 'text-zinc-400'}`}>Secure payment via ABA PayWay</p>
          <div className="flex items-center justify-center gap-4 mt-3 flex-wrap">
            {["ABA Pay", "KHQR", "Visa", "MasterCard", "WeChat Pay", "Alipay"].map(m => (
              <span key={m} className={`text-[10px] px-3 py-1.5 rounded-lg font-medium ${d ? 'bg-zinc-800 text-zinc-400 border border-zinc-700' : 'bg-white text-zinc-500 border border-zinc-200 shadow-sm'}`}>{m}</span>
            ))}
          </div>
        </div>

        {/* FAQ */}
        <div className="mt-16 max-w-2xl mx-auto">
          <h2 className={`text-xl font-semibold tracking-tight text-center mb-6 ${d ? 'text-white' : 'text-zinc-900'}`} style={{ fontFamily: "'Outfit', sans-serif" }}>
            FAQ
          </h2>
          <div className="space-y-3">
            {[
              { q: "What happens when my videos run out?", a: "You can upgrade your plan anytime to get more videos. Unused videos do not roll over." },
              { q: "Can I cancel anytime?", a: "Yes. Your plan stays active until the end of the billing period." },
              { q: "How do I receive my dubbed videos?", a: "Connect your Telegram. All dubbed videos are sent directly to your Telegram chat." },
              { q: "What payment methods are accepted?", a: "ABA Pay, KHQR, Visa, MasterCard, WeChat Pay, and Alipay via ABA PayWay." },
              { q: "What is priority queue?", a: "Pro and Business users' videos are processed first, before Free and Basic users." },
            ].map((faq, i) => (
              <div key={i} className={`p-4 rounded-xl border ${d ? 'bg-zinc-900/40 border-zinc-800/50' : 'bg-white border-zinc-200'}`}>
                <div className={`text-sm font-semibold ${d ? 'text-zinc-200' : 'text-zinc-800'}`}>{faq.q}</div>
                <div className={`text-xs mt-1 ${d ? 'text-zinc-500' : 'text-zinc-500'}`}>{faq.a}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const Feature = ({ d, ok, text }) => (
  <div className="flex items-center gap-2.5">
    {ok ? (
      <div className={`w-5 h-5 rounded-full flex items-center justify-center ${d ? 'bg-emerald-500/15' : 'bg-emerald-100'}`}>
        <Check className="w-3 h-3 text-emerald-500" weight="bold" />
      </div>
    ) : (
      <div className={`w-5 h-5 rounded-full flex items-center justify-center ${d ? 'bg-zinc-800' : 'bg-zinc-100'}`}>
        <X className="w-3 h-3 text-zinc-400" weight="bold" />
      </div>
    )}
    <span className={`text-xs ${ok ? (d ? 'text-zinc-300' : 'text-zinc-700') : (d ? 'text-zinc-600' : 'text-zinc-400')}`}>{text}</span>
  </div>
);

export default PricingPage;
