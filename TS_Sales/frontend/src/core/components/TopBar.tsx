'use client';

import Link from 'next/link';

export default function TopBar() {

    return (
        <header className="h-16 bg-white shadow-md flex items-center justify-between px-8 border-b-2 border-primary-200">
            <div className="flex-1 flex items-center gap-6">
                <h2 className="text-lg font-semibold text-primary-700">TS_SALES - Hệ thống Xuất khẩu</h2>
                <Link
                    href="/public-site"
                    className="ml-4 px-4 py-2 bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200 font-semibold text-sm transition-colors"
                >
                    🌾 Xem trang chủ
                </Link>
            </div>

            <div className="flex items-center gap-6">
                <button className="relative text-gray-600 hover:text-gray-900">
                    <span className="text-xl">🔔</span>
                    <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
                </button>

                <div className="border-l border-gray-200 pl-6">
                    <div className="flex items-center gap-3">
                        <div className="text-right">
                            <p className="text-sm font-medium text-gray-800">Nguyễn Văn A</p>
                            <p className="text-xs text-gray-500">Sales Manager</p>
                        </div>
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-bold">
                            NV
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
}
