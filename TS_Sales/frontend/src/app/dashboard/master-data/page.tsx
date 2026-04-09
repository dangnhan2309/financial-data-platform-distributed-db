import DashboardLayout from '@core/layouts/DashboardLayout';
import MasterDataDashboard from '@modules/master_data/views/MasterDataDashboard';

export default function MasterDataPage() {
    return (
        <DashboardLayout>
            <MasterDataDashboard />
        </DashboardLayout>
    );
}
