import DashboardLayout from '@core/layouts/DashboardLayout';
import ContractDashboard from '@modules/contract/views/ContractDashboard';

export default function ContractPage() {
    return (
        <DashboardLayout>
            <ContractDashboard />
        </DashboardLayout>
    );
}
