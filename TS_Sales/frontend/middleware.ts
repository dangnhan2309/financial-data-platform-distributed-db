import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
    // Redirect / → /dashboard
    if (request.nextUrl.pathname === '/') {
        return NextResponse.redirect(new URL('/dashboard', request.url));
    }

    // TODO: Thêm auth check ở đây sau
    // if (!isAuthenticated && request.nextUrl.pathname.startsWith('/dashboard')) {
    //     return NextResponse.redirect(new URL('/login', request.url));
    // }

    return NextResponse.next();
}

export const config = {
    matcher: [
        /*
         * Match all request paths except for the ones starting with:
         * - api (API routes)
         * - _next/static (static files)
         * - _next/image (image optimization files)
         * - favicon.ico (favicon file)
         */
        '/((?!api|_next/static|_next/image|favicon.ico).*)',
    ],
};
