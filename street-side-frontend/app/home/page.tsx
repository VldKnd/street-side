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
          {`Why does this app exists ?`}
        </p>
      </div>
      <div>
        <p className="text-foreground-white text-sm indent-8">
          Each clearing center distributes public, quarterly reports on its financial health, which must comply with the reporting rules recommended by the Bank of International Settlements. In practice, the reports are issued at different times, in different formats and are not centralized for quick analysis. This variety of documents increases the time required to analyze them.
        </p>
      </div>
      <div>
        <p className="text-foreground-white text-sm indent-8 mt-3">
          This process can be simply automated.  In addition, clearing reports do not send email or other notifications. There are errors in reports that can be automatically caught. In general, such documents are inconvenient to work with. With the help of automatic collection of data from multiple clearing centers and cross-analysis of their state on the basis of specified risk management parameters - it is possible to improve the quality of risk management and dialog between venues and their clients.
        </p>
      </div>
      <InLineListOfCompanies/>
    </div>
  );
}
