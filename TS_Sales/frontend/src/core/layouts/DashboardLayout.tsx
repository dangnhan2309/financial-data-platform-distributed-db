'use client';

import Sidebar from '../components/Sidebar';
import TopBar from '../components/TopBar';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex h-screen bg-gray-50">
            <Sidebar />
            <div className="flex-1 flex flex-col border-l-4 border-primary-300">
                <TopBar />
                <main className="flex-1 overflow-auto p-8">
                    {children}
                </main>
            </div>
        </div>
    );
}
