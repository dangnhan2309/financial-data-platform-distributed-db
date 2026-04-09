'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

interface SidebarItem {
    label: string;
    href: string;
    icon: string;
    children?: SidebarItem[];
}

const sidebarItems: SidebarItem[] = [
    { label: 'Dashboard', href: '/dashboard', icon: '📊' },
    {
        label: 'Quản lý Dữ liệu',
        icon: '📋',
        href: '#',
        children: [
            { label: 'Nhân viên', href: '/dashboard/master-data/staff', icon: '👤' },
            { label: 'Khách hàng', href: '/dashboard/master-data/customers', icon: '🏢' },
            { label: 'Sản phẩm', href: '/dashboard/master-data/products', icon: '📦' },
            { label: 'Điều khoản thanh toán', href: '/dashboard/master-data/payment-terms', icon: '💳' },
            { label: 'Incoterm', href: '/dashboard/master-data/incoterms', icon: '🚢' },
        ],
    },
    {
        label: 'Bán hàng',
        icon: '💰',
        href: '#',
        children: [
            { label: 'Báo giá Kỹ thuật', href: '/dashboard/quotation', icon: '📄' },
            { label: 'Hóa đơn tạm tính', href: '/dashboard/proforma-invoice', icon: '📋' },
            { label: 'Hợp đồng', href: '/dashboard/contract', icon: '📝' },
            { label: 'Đơn hàng', href: '/dashboard/sale-order', icon: '🛒' },
        ],
    },
    {
        label: 'Xuất khẩu',
        icon: '✈️',
        href: '#',
        children: [
            { label: 'Bộ chứng từ XK', href: '/dashboard/export-document', icon: '📑' },
            { label: 'Lịch trình tàu', href: '/dashboard/shipment', icon: '⛴️' },
        ],
    },
    {
        label: 'Công cụ DB',
        icon: '🔧',
        href: '/dashboard/oracle-execution',
    },
];

export default function Sidebar() {
    const [expandedItems, setExpandedItems] = useState<string[]>(['Bán hàng']);
    const router = useRouter();

    const toggleExpand = (label: string) => {
        setExpandedItems((prev) =>
            prev.includes(label) ? prev.filter((item) => item !== label) : [...prev, label]
        );
    };

    return (
        <aside className="w-64 bg-gradient-to-b from-primary-700 to-primary-900 text-white shadow-lg">
            <div className="p-6">
                <Link href="/" className="flex items-center gap-2 font-bold text-xl">
                    <span className="text-3xl">🌾</span>
                    <span>GC Food</span>
                </Link>
                <p className="text-sm text-primary-200 mt-1">TS_SALES Dashboard</p>
            </div>

            <nav className="flex-1 overflow-y-auto">
                {sidebarItems.map((item) => (
                    <div key={item.label}>
                        {item.children ? (
                            <>
                                <button
                                    onClick={() => toggleExpand(item.label)}
                                    className="w-full flex items-center justify-between px-6 py-3 hover:bg-primary-600 transition-colors"
                                >
                                    <div className="flex items-center gap-3">
                                        <span>{item.icon}</span>
                                        <span>{item.label}</span>
                                    </div>
                                    <span className={`transition-transform ${expandedItems.includes(item.label) ? 'rotate-180' : ''}`}>
                                        ▼
                                    </span>
                                </button>
                                {expandedItems.includes(item.label) && (
                                    <div className="bg-primary-800">
                                        {item.children.map((child) => (
                                            <Link
                                                key={child.href}
                                                href={child.href}
                                                className="flex items-center gap-3 px-10 py-2 text-sm hover:bg-primary-700 transition-colors"
                                            >
                                                <span>{child.icon}</span>
                                                <span>{child.label}</span>
                                            </Link>
                                        ))}
                                    </div>
                                )}
                            </>
                        ) : (
                            <Link
                                href={item.href}
                                className="flex items-center gap-3 px-6 py-3 hover:bg-primary-600 transition-colors"
                            >
                                <span>{item.icon}</span>
                                <span>{item.label}</span>
                            </Link>
                        )}
                    </div>
                ))}
            </nav>

            <div className="border-t border-primary-600 p-6">
                <button
                    onClick={() => {
                        localStorage.removeItem('authToken');
                        router.push('/');
                    }}
                    className="w-full text-left text-sm text-primary-200 hover:text-white transition-colors"
                >
                    🚪 Đăng xuất
                </button>
            </div>
        </aside>
    );
}
