import type { Metadata } from 'next';
// @ts-ignore - CSS imports are handled by Next.js
import './globals.css';

export const metadata: Metadata = {
    title: 'GC Food - TS_SALES System',
    description: 'Frontend for GC Food Export Sales Management System',
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="vi">
            <head>
                <meta charSet="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
            </head>
            <body className="bg-gray-100">
                {children}
            </body>
        </html>
    );
}
