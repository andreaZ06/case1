import { describe, expect, it } from 'vitest';

import { md5 } from '@/shared/lib/hash';

describe('md5', () => {
  it('returns the standard hex digest for a string', () => {
    expect(md5('hello')).toBe('5d41402abc4b2a76b9719d911017c592');
  });

  it('returns the standard hex digest for binary input', () => {
    const bytes = new TextEncoder().encode('hello');

    expect(md5(bytes)).toBe('5d41402abc4b2a76b9719d911017c592');
  });
});
