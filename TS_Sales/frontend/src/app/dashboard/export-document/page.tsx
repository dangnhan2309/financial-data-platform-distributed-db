import DashboardLayout from '@core/layouts/DashboardLayout';
import ExportDocumentDashboard from '@modules/export_document/views/ExportDocumentDashboard';

export default function ExportDocumentPage() {
    return (
        <DashboardLayout>
            <ExportDocumentDashboard />
        </DashboardLayout>
    );
}
