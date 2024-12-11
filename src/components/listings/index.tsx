import type { ReactNode } from 'react';
import Listing, { type Result } from '@/components/listing';

export default function Listings({ results }: { results: Result[] }): ReactNode {
    console.log('<Listings results={results} />:\n', results);
    const listings: ReactNode[] = results.map((r: Result) => (<Listing key={r.id} result={r} />));
// ul classes: grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 sm:gap-x-6 lg:grid-cols-4 xl:gap-x-8
    return (
        <div className="w-full max-w-2xl space-y-4">
            {listings}
        </div>
    );
}
