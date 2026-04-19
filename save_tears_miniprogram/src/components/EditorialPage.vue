<template>
  <view class="editorial-page" :class="[compact ? 'editorial-page--compact' : '', `editorial-page--${tone}`]">
    <view class="editorial-page__wash"></view>
    <view class="editorial-page__wave editorial-page__wave--top"></view>
    <view class="editorial-page__wave editorial-page__wave--mid"></view>
    <view class="editorial-page__wave editorial-page__wave--bottom"></view>
    <view class="editorial-page__caustic editorial-page__caustic--top"></view>
    <view class="editorial-page__caustic editorial-page__caustic--mid"></view>
    <view class="editorial-page__orb editorial-page__orb--top"></view>
    <view class="editorial-page__orb editorial-page__orb--side"></view>
    <view class="editorial-page__orb editorial-page__orb--bottom"></view>
    <view class="editorial-page__content">
      <slot />
    </view>
  </view>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    tone?: 'mist' | 'deep' | 'warm';
    compact?: boolean;
  }>(),
  {
    tone: 'mist',
    compact: false,
  },
);
</script>

<style scoped>
.editorial-page {
  position: relative;
  min-height: 100vh;
  padding: 34rpx var(--st-page-padding) var(--st-page-bottom);
  overflow: hidden;
}

.editorial-page--compact {
  padding-top: 22rpx;
}

.editorial-page--mist {
  background:
    radial-gradient(circle at 85% 12%, rgba(255, 255, 255, 0.84) 0, rgba(255, 255, 255, 0) 18%),
    linear-gradient(180deg, #f7fbff 0%, #edf6ff 46%, #e2f0fd 100%);
}

.editorial-page--deep {
  background:
    radial-gradient(circle at 12% 12%, rgba(255, 255, 255, 0.68) 0, rgba(255, 255, 255, 0) 18%),
    linear-gradient(180deg, #f4fbff 0%, #e8f4ff 42%, #dcebfb 100%);
}

.editorial-page--warm {
  background:
    radial-gradient(circle at 88% 10%, rgba(255, 255, 255, 0.82) 0, rgba(255, 255, 255, 0) 18%),
    linear-gradient(180deg, #f7fbff 0%, #eef6ff 46%, #e3f0fb 100%);
}

.editorial-page__wash {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.28) 0%, rgba(255, 255, 255, 0) 18%),
    linear-gradient(90deg, rgba(255, 255, 255, 0.16) 0%, rgba(255, 255, 255, 0) 24%, rgba(255, 255, 255, 0.12) 100%);
  pointer-events: none;
}

.editorial-page__wave {
  position: absolute;
  left: -24%;
  width: 148%;
  border-radius: 50%;
  pointer-events: none;
  filter: blur(12rpx);
  opacity: 0.72;
}

.editorial-page__wave--top {
  top: 42rpx;
  height: 240rpx;
  background: radial-gradient(
    ellipse at 50% 46%,
    rgba(121, 201, 255, 0.24) 0%,
    rgba(121, 201, 255, 0.14) 34%,
    rgba(121, 201, 255, 0.04) 60%,
    rgba(121, 201, 255, 0) 76%
  );
  animation: st-water-swell-up 9.8s ease-in-out infinite;
}

.editorial-page__wave--mid {
  top: 288rpx;
  height: 284rpx;
  background: radial-gradient(
    ellipse at 50% 52%,
    rgba(103, 190, 255, 0.2) 0%,
    rgba(103, 190, 255, 0.12) 36%,
    rgba(103, 190, 255, 0.03) 62%,
    rgba(103, 190, 255, 0) 78%
  );
  animation: st-water-swell-down 11.2s ease-in-out infinite;
}

.editorial-page__wave--bottom {
  bottom: 18rpx;
  height: 300rpx;
  background: radial-gradient(
    ellipse at 50% 54%,
    rgba(134, 209, 255, 0.18) 0%,
    rgba(134, 209, 255, 0.1) 38%,
    rgba(134, 209, 255, 0.03) 64%,
    rgba(134, 209, 255, 0) 80%
  );
  animation: st-water-swell-up 12.6s ease-in-out infinite reverse;
}

.editorial-page__caustic {
  position: absolute;
  left: -10%;
  width: 120%;
  height: 86rpx;
  border-radius: 999rpx;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.22) 40%,
    rgba(255, 255, 255, 0.08) 54%,
    rgba(255, 255, 255, 0) 100%
  );
  filter: blur(10rpx);
  opacity: 0.54;
  pointer-events: none;
}

.editorial-page__caustic--top {
  top: 128rpx;
  animation: st-water-caustic 8.6s ease-in-out infinite;
}

.editorial-page__caustic--mid {
  top: 412rpx;
  height: 96rpx;
  opacity: 0.42;
  animation: st-water-caustic 10.8s ease-in-out infinite reverse;
}

.editorial-page__orb {
  position: absolute;
  border-radius: 999rpx;
  filter: blur(14rpx);
  animation: st-orb-float 8.5s ease-in-out infinite;
}

.editorial-page__orb--top {
  top: -56rpx;
  right: 12rpx;
  width: 220rpx;
  height: 220rpx;
  background: rgba(139, 212, 255, 0.26);
}

.editorial-page__orb--side {
  top: 360rpx;
  right: -84rpx;
  width: 240rpx;
  height: 300rpx;
  background: rgba(47, 140, 255, 0.16);
  animation-delay: 1.8s;
}

.editorial-page__orb--bottom {
  bottom: 180rpx;
  left: -90rpx;
  width: 260rpx;
  height: 220rpx;
  background: rgba(139, 212, 255, 0.22);
  animation-delay: 3.1s;
}

.editorial-page__content {
  position: relative;
  z-index: 1;
}
</style>
