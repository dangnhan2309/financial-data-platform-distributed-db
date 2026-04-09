import DashboardLayout from '@core/layouts/DashboardLayout';
import OracleExecutionHub from '@modules/oracle_execution/views/OracleExecutionHub';

export default function OracleExecutionPage() {
    return (
        <DashboardLayout>
            <OracleExecutionHub />
        </DashboardLayout>
    );
}
