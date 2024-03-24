import CompanySelector from '@/app/raw/components/CompanySelector';
import DocumentSelector from '@/app/raw/components/DocumentSelector';
import DownloadPeriodComponent from '@/app/raw/components/DownloadPeriodComponent';
import Document from '@/app/raw/components/Document';

export default async function Home() {
  return (
    <div className='h-full w-4/6'>
      <CompanySelector />

      <div className='flex mt-5'>
        <DocumentSelector />
        <div className="grow" />
        <DownloadPeriodComponent />
      </div>
      <Document />
    </div>
  );
}
