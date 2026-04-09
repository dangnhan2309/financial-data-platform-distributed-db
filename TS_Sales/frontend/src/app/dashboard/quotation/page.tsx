import DashboardLayout from '@core/layouts/DashboardLayout';
import QuotationDashboard from '@modules/quotation/views/QuotationDashboard';

export default function QuotationPage() {
    return (
        <DashboardLayout>
            <QuotationDashboard />
        </DashboardLayout>
    );
}
