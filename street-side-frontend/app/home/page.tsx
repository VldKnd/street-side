'use client';
import InLineListOfCompanies from './inLineListOfCompanies';

export default function Home() {

  return (
    <div className='h-full w-4/6'>
      <div className='mb-10 ml-3'>
        <p className='font-bold text-company-grey text-2xl'>
          {`Welcome to the streets!`}
        </p>
      </div>
      <div className='mb-3 ml-3'>
        <p className='font-bold text-company-grey text-foreground-white'>
          {`Why does this app exist?`}
        </p>
      </div>
      <div>
        <p className="text-foreground-white text-sm indent-8">
        Each clearing center issues public quarterly reports on its financial status, adhering to reporting standards recommended by the Bank for International Settlements. However, these reports are dispersed across different times and formats, lacking centralization for efficient analysis. This diversity complicates the analysis process and prolongs the time required for thorough examination.
        </p>
      </div>
      <div>
        <p className="text-foreground-white text-sm indent-8 mt-3">
        Automating this process is straightforward and beneficial. Current clearing reports lack mechanisms for email notifications, leaving potential errors unchecked. Consequently, working with such documents proves inconvenient. By implementing automated data collection from various clearing centers and conducting cross-analysis based on predefined risk management parameters, we can significantly enhance risk management quality and foster improved communication between venues and their clientele.
        </p>
      </div>
      <InLineListOfCompanies/>
    </div>
  );
}
