
import LoadingCompanySelector from './components/loading/LoadingCompanySelector';

export default async function Home() {
    return (
        <div className='h-full w-4/6'>
            <LoadingCompanySelector />
        </div>
    );
}
