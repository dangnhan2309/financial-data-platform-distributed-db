'use client';

import React from 'react';

interface DataTableColumn<T> {
    header: string;
    accessor: (item: T) => React.ReactNode;
    width?: string;
}

interface DataTableProps<T> {
    columns: DataTableColumn<T>[];
    data: T[];
    onRowClick?: (item: T, index: number) => void;
    isLoading?: boolean;
    emptyMessage?: string;
}

export default function DataTable<T>({
    columns,
    data,
    onRowClick,
    isLoading = false,
    emptyMessage = 'Không có dữ liệu',
}: DataTableProps<T>) {
    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    if (data.length === 0) {
        return (
            <div className="flex justify-center items-center h-64 text-gray-500">
                <p>{emptyMessage}</p>
            </div>
        );
    }

    return (
        <div className="overflow-x-auto shadow-md rounded-lg">
            <table className="w-full border-collapse">
                <thead className="bg-primary-600 text-white">
                    <tr>
                        {columns.map((col, idx) => (
                            <th
                                key={idx}
                                className="px-6 py-3 text-left text-sm font-semibold"
                                style={{ width: col.width }}
                            >
                                {col.header}
                            </th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.map((item, rowIdx) => (
                        <tr
                            key={rowIdx}
                            onClick={() => onRowClick?.(item, rowIdx)}
                            className={`border-b border-gray-200 ${onRowClick ? 'cursor-pointer hover:bg-gray-50' : ''}`}
                        >
                            {columns.map((col, colIdx) => (
                                <td key={colIdx} className="px-6 py-4 text-sm text-gray-700">
                                    {col.accessor(item)}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
