import PublicLayout from '@core/layouts/PublicLayout';
import PublicSitePage from '@modules/public_site/page';

export default function PublicSite() {
    return (
        <PublicLayout>
            <PublicSitePage />
        </PublicLayout>
    );
}
