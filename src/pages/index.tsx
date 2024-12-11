import Head from 'next/head';
import Image from 'next/image';
import { ChangeEvent, FormEvent, useState } from 'react';
import type { ReactNode } from 'react';
import Listings from '@/components/listings';
import { type Result } from '@/components/listing';
// remove after testing:
import { mockResults } from './data';

const metadata = {
    charset: 'UTF-8',
    description: 'Find books on BookFinder',
    title: 'BookFinder | Search Books',
    viewport: 'initial-scale=1.0, width=device-width'
};

export default function Home(): ReactNode {
    async function handleSubmit(e: FormEvent) {
        try {
            e.preventDefault();
            e.persist && e.persist();

            const terms = encodeURIComponent(searchTerms.replaceAll(' ', '+'));

            console.log('Terms:', terms);

            // const response = await fetch('');
            // const results: Result[] = await response.json();

            // setResults(results);
            setResults(mockResults);
        } catch (err) {
            if (err instanceof Error) {
                console.error(err.message);
            } else {
                console.error('An unknown error occurred');
            }
        }

    }

    async function handleChange(e: ChangeEvent) {
        try {
            e.preventDefault();
            e.persist && e.persist();

            const value = (e.target as HTMLInputElement).value;

            setSearchTerms(value.trim());
        } catch (err) {
            if (err instanceof Error) {
                console.error(err.message);
            } else {
                console.error('An unknown error occurred');
            }
        }
    };

    const [searchTerms, setSearchTerms] = useState('');

    const [results, setResults] = useState<Result[]>([]);

    return (
        <div className="min-h-24 flex flex-col items-center justify-center p-4">
            <Head>
                <title>{metadata.title}</title>
                <meta charSet={metadata.charset} />
                <meta name="description" content={metadata.description} />
                <meta name="viewport" content={metadata.viewport} />
            </Head>

            <header className="min-h-40">
                <Image
                    alt="Company Logo"
                    className=""
                    width={461}
                    height={70}
                    src="/logo.svg"
                    priority
                />
                <h2 className="text-right text-[#8d1a6e] font-bold">Find your next read</h2>
            </header>

            <main className="min-h-screen bg-gray-100 p-4">
                <div className="flex flex-col items-center space-y-6">
                    <div className="w-full max-w-2xl">
                        <div className="relative">
                            <form onSubmit={handleSubmit}>
                                <input
                                    type="text"
                                    placeholder="Enter book title, author, or ISBN"
                                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
                                    onChange={handleChange}
                                />
                                <button type="submit" className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700">
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>
                                </button>
                            </form>
                        </div>
                    </div>
                </div>

                <div id="results" className="my-4">
                    <Listings results={results} />
                </div>
            </main>

            <footer className="mt-8 text-center text-sm text-gray-500">
                <p>&copy; 2024-Present BookFinder. All rights reserved.</p>
            </footer>
        </div>
    );
}
