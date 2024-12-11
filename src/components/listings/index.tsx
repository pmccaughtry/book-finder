import type { ReactNode } from 'react';
import Listing, { type Result } from '@/components/listing';

export default function Listings({ results }: { results: Result[] }): ReactNode {
    const listings: ReactNode[] = results.map((r: Result) => (<Listing key={r.id} result={r} />));

    return (
        <div className="w-full max-w-2xl space-y-4">
            {listings}
        </div>
    );
}
