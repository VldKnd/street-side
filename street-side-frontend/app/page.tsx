import CompanySelector from './components/CompanySelector';
import DocumentSelector from './components/DocumentSelector';
import DownloadPeriodComponent from './components/DownloadPeriodComponent';
import Document from './components/Document';
export default async function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className='h-full w-4/6'>
        <CompanySelector />
        <div className='flex mt-5'>
          <DocumentSelector />
          <div className="grow" />
          <DownloadPeriodComponent />
        </div>
        <Document />
      </div>
    </main>
  );
}
