
import LoadingCompanySelector from './components/loading/LoadingCompanySelector';
import LoadingDocumentSelector from '@/app/raw/components/loading/LoadingDocumentSelector';
import LoadingDownloadPeriodComponent from '@/app/raw/components/loading/LoadingDownloadPeriodComponent';

export default async function Home() {
    return (
        <div className='h-full w-4/6'>
            <LoadingCompanySelector />
            <div className='flex mt-5'>
                <LoadingDocumentSelector />
                <div className="grow" />
                <LoadingDownloadPeriodComponent />
            </div>
        </div>
    );
}
