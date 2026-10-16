import { expect, test } from 'bun:test'

import { VOICE_PIPELINE } from './pipeline'

test('fixed pipeline describes the Cartesia voice agent', () => {
  expect(Object.isFrozen(VOICE_PIPELINE)).toBe(true)
  expect(VOICE_PIPELINE.provider).toBe('Cartesia')
  expect(VOICE_PIPELINE.title).toBe('Real-time Voice Agent')
  expect(VOICE_PIPELINE.eyebrow).toBe('Developer showcase')
  expect(VOICE_PIPELINE.stt).toBe('Sarvam STT (en-IN)')
  expect(VOICE_PIPELINE.llm).toBe('OpenAI GPT-4o mini')
  expect(VOICE_PIPELINE.tts).toBe('Cartesia Sonic 3.6 (Skylar)')
})
