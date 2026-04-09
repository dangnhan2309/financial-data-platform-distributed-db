import DashboardLayout from '@core/layouts/DashboardLayout';
import SaleOrderDashboard from '@modules/sale_order/views/SaleOrderDashboard';

export default function SaleOrderPage() {
    return (
        <DashboardLayout>
            <SaleOrderDashboard />
        </DashboardLayout>
    );
}
