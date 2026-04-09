'use client';

export default function PublicLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-white">
            <nav className="bg-white shadow-sm">
                <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
                    <div className="flex items-center gap-2 font-bold text-2xl">
                        <span className="text-4xl">🌾</span>
                        <span className="text-primary-700">GC Food</span>
                    </div>
                    <div className="flex gap-8">
                        <a href="#about" className="text-gray-700 hover:text-primary-600">Giới thiệu</a>
                        <a href="#products" className="text-gray-700 hover:text-primary-600">Sản phẩm</a>
                        <a href="#contact" className="text-gray-700 hover:text-primary-600">Liên hệ</a>
                        <a href="/dashboard" className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700">
                            B2B Portal
                        </a>
                    </div>
                </div>
            </nav>
            {children}
        </div>
    );
}
