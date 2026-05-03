import React from "react";

type IconProps = { size?: number; color?: string };

export const VercelLogo: React.FC<IconProps> = ({ size = 120, color = "#fff" }) => (
  <svg width={size} height={size * 0.87} viewBox="0 0 76 65" fill="none">
    <path d="M37.5274 0L75.0548 65H0L37.5274 0Z" fill={color} />
  </svg>
);

export const NextLogo: React.FC<IconProps> = ({ size = 120, color = "#fff" }) => (
  <svg width={size} height={size} viewBox="0 0 180 180" fill="none">
    <mask id="maskN" maskUnits="userSpaceOnUse" x="0" y="0" width="180" height="180">
      <circle cx="90" cy="90" r="90" fill="black" />
    </mask>
    <g mask="url(#maskN)">
      <circle cx="90" cy="90" r="87" fill="black" stroke={color} strokeWidth="6" />
      <path
        d="M149.508 157.52L69.142 54H54V125.97H66.1136V69.3836L139.999 164.845C143.333 162.614 146.509 160.165 149.508 157.52Z"
        fill={color}
      />
      <rect x="115" y="54" width="12" height="72" fill={color} />
    </g>
  </svg>
);

export const GoogleLogo: React.FC<IconProps> = ({ size = 120 }) => (
  <svg width={size} height={size} viewBox="0 0 48 48">
    <path
      fill="#4285F4"
      d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
    />
    <path
      fill="#34A853"
      d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
    />
    <path
      fill="#FBBC05"
      d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
    />
    <path
      fill="#EA4335"
      d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
    />
  </svg>
);

export const HackerIcon: React.FC<IconProps> = ({ size = 120, color = "#EF4444" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path
      d="M12 2a5 5 0 0 0-5 5v2a5 5 0 1 0 10 0V7a5 5 0 0 0-5-5Z"
      fill={color}
      opacity="0.9"
    />
    <path
      d="M4 22c0-4.4 3.6-8 8-8s8 3.6 8 8"
      stroke={color}
      strokeWidth="2.5"
      strokeLinecap="round"
      fill="none"
    />
    <rect x="8" y="7" width="2.5" height="2.5" rx="0.5" fill="#0A0E27" />
    <rect x="13.5" y="7" width="2.5" height="2.5" rx="0.5" fill="#0A0E27" />
  </svg>
);

export const ShieldIcon: React.FC<IconProps> = ({ size = 120, color = "#EF4444" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path
      d="M12 2 3 5v7c0 5 3.8 9.7 9 10 5.2-.3 9-5 9-10V5l-9-3Z"
      fill={color}
      opacity="0.15"
      stroke={color}
      strokeWidth="1.8"
    />
    <path
      d="M9 12l2 2 4-4"
      stroke={color}
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
  </svg>
);

export const KeyIcon: React.FC<IconProps> = ({ size = 120, color = "#FDE047" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <circle cx="8" cy="12" r="4" stroke={color} strokeWidth="2.5" fill="none" />
    <path
      d="M12 12h9m-3 0v3m-3-3v3"
      stroke={color}
      strokeWidth="2.5"
      strokeLinecap="round"
    />
  </svg>
);

export const OAuthIcon: React.FC<IconProps> = ({ size = 120, color = "#22D3EE" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <rect x="4" y="10" width="16" height="10" rx="2" fill={color} opacity="0.2" stroke={color} strokeWidth="2" />
    <path
      d="M8 10V7a4 4 0 0 1 8 0v3"
      stroke={color}
      strokeWidth="2.2"
      strokeLinecap="round"
      fill="none"
    />
    <circle cx="12" cy="15" r="1.6" fill={color} />
  </svg>
);

export const ContextIcon: React.FC<IconProps> = ({ size = 120, color = "#A78BFA" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <rect x="3" y="4" width="18" height="16" rx="3" stroke={color} strokeWidth="2" fill={color} fillOpacity="0.15" />
    <circle cx="12" cy="11" r="2" fill={color} />
    <path d="M8 16c0-1.8 1.8-3 4-3s4 1.2 4 3" stroke={color} strokeWidth="2" fill="none" />
    <path d="M7 8l-2-2M17 8l2-2" stroke={color} strokeWidth="2" strokeLinecap="round" />
  </svg>
);

export const WarningIcon: React.FC<IconProps> = ({ size = 40, color = "#EF4444" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path
      d="M12 2 2 21h20L12 2Z"
      fill={color}
      opacity="0.9"
    />
    <path d="M12 9v5M12 17v.5" stroke="#0A0E27" strokeWidth="2.2" strokeLinecap="round" />
  </svg>
);

export const LiveDotIcon: React.FC<IconProps> = ({ size = 14, color = "#fff" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="6" fill={color} />
  </svg>
);

export const IconByName: React.FC<{ name: string; size?: number }> = ({ name, size = 120 }) => {
  switch (name) {
    case "vercel":
      return <VercelLogo size={size} />;
    case "nextjs":
      return <NextLogo size={size} />;
    case "google":
      return <GoogleLogo size={size} />;
    case "hacker":
      return <HackerIcon size={size} />;
    case "shield":
      return <ShieldIcon size={size} />;
    case "oauth":
      return <OAuthIcon size={size} />;
    case "context":
      return <ContextIcon size={size} />;
    case "key":
      return <KeyIcon size={size} />;
    default:
      return null;
  }
};
