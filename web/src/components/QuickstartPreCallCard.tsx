'use client'

import { ArrowRight, AudioLines, Bot, CheckCircle2, Code2, Loader2, Mic2, Radio, Sparkles } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { VOICE_PIPELINE } from '@/lib/pipeline'

type QuickstartPreCallCardProps = {
  isLoading: boolean
  error: string | null
  onStartConversation: () => void
}

export function QuickstartPreCallCard({ isLoading, error, onStartConversation }: QuickstartPreCallCardProps) {
  return (
    <div className="mx-auto w-full max-w-[76rem] animate-fade-up px-1">
      <div className="overflow-hidden rounded-[2rem] border border-border/70 bg-card/80 shadow-[0_36px_120px_rgba(15,23,42,0.14)] backdrop-blur-xl">
        <div className="flex items-center justify-between gap-4 border-b border-border/70 px-6 py-4 sm:px-8">
          <div className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.18em] text-primary">
            <Code2 className="h-4 w-4" /> {VOICE_PIPELINE.eyebrow}
          </div>
          <div className="hidden items-center gap-2 font-mono text-[11px] text-muted-foreground sm:flex">
            <span className="h-2 w-2 rounded-full bg-rose-500" /> fixed-pipeline / rtc + rtm
          </div>
        </div>
        <div className="grid lg:grid-cols-[1.05fr_0.95fr]">
          <section className="flex flex-col justify-center px-6 py-10 text-left sm:px-10 sm:py-14 lg:px-14 lg:py-16">
            <div className="mb-6 inline-flex w-fit items-center gap-2 rounded-full border border-primary/20 bg-primary/10 px-3 py-1.5 text-xs font-semibold text-primary">
              <Sparkles className="h-3.5 w-3.5" /> {VOICE_PIPELINE.accent}
            </div>
            <p className="text-sm font-semibold text-muted-foreground">{VOICE_PIPELINE.provider}</p>
            <h1 className="mt-2 max-w-2xl text-4xl font-semibold leading-[1.02] tracking-[-0.045em] text-foreground sm:text-5xl">
              Build with voice. Observe every turn.
            </h1>
            <p className="mt-6 max-w-xl text-base leading-7 text-muted-foreground">
              A transcript-first reference experience for testing real-time speech recognition, agent reasoning, and
              synthesized response audio.
            </p>
            <div className="mt-8 flex flex-wrap gap-x-5 gap-y-3 text-xs font-medium text-muted-foreground">
              {['Live interim transcripts', 'Pipeline latency metrics', 'Exportable session log'].map((item) => (
                <span key={item} className="flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-rose-500" /> {item}
                </span>
              ))}
            </div>

            <Button
              onClick={onStartConversation}
              disabled={isLoading}
              className="mt-9 h-12 w-full rounded-xl px-5 text-sm font-semibold shadow-[0_14px_36px_hsl(var(--primary)/0.24)] sm:w-fit"
              aria-label={isLoading ? 'Starting conversation with AI agent' : 'Start conversation with AI agent'}
            >
              {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Mic2 className="h-4 w-4" />}
              {isLoading ? 'Preparing session...' : 'Launch voice session'}
              {!isLoading ? <ArrowRight className="h-4 w-4" /> : null}
            </Button>
            {error ? (
              <p className="mt-3 text-sm font-medium text-destructive" role="alert">
                {error}
              </p>
            ) : null}
          </section>

          <aside className="relative flex flex-col justify-between overflow-hidden border-t border-border/70 bg-slate-950 px-7 py-9 text-slate-100 sm:px-10 sm:py-12 lg:border-l lg:border-t-0">
            <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-rose-500/20 blur-3xl" />
            <div className="absolute -bottom-24 -left-20 h-64 w-64 rounded-full bg-amber-400/15 blur-3xl" />
            <div className="relative">
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-amber-300">Execution path</p>
              <div className="mt-6 space-y-3">
                {[
                  { icon: Radio, label: 'Speech to text', value: VOICE_PIPELINE.stt },
                  { icon: Bot, label: 'Reasoning', value: VOICE_PIPELINE.llm },
                  { icon: AudioLines, label: 'Text to speech', value: VOICE_PIPELINE.tts },
                ].map(({ icon: Icon, label, value }) => (
                  <div
                    key={label}
                    className="flex items-center gap-4 rounded-2xl border border-white/10 bg-white/[0.04] p-4"
                  >
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-rose-400/10 text-rose-300">
                      <Icon className="h-4 w-4" />
                    </div>
                    <div>
                      <p className="text-xs text-slate-400">{label}</p>
                      <p className="mt-0.5 text-sm font-semibold text-slate-100">{value}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <p className="relative mt-8 text-xs leading-5 text-slate-400">
              {VOICE_PIPELINE.description} Microphone permission is requested when you start.
            </p>
          </aside>
        </div>
      </div>
    </div>
  )
}
