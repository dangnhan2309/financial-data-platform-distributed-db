import DashboardLayout from '@core/layouts/DashboardLayout';
import ProformaInvoiceDashboard from '@modules/proforma_invoice/views/ProformaInvoiceDashboard';

export default function ProformaInvoicePage() {
    return (
        <DashboardLayout>
            <ProformaInvoiceDashboard />
        </DashboardLayout>
    );
}
