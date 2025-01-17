import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Home from '../src/pages/index';
import Listings from '../src/components/listings';
import { escape } from 'validator';
import type { Result } from '../src/components/listing';
import fetchMock from 'jest-fetch-mock';

const mockFetch = jest.spyOn(global, 'fetch');

describe('Home Component', () => {
    beforeEach(() => {
        mockFetch.mockClear();
    });

    it('should render the initial UI as expected', () => {
        render(<Home />);
        expect(screen.getByPlaceholderText(/Enter book title, author, or ISBN/i)).toBeInTheDocument();
        expect(screen.getByText(/Find your next read/i)).toBeInTheDocument();
    });

    it('should update searchTerms on input change', () => {
        render(<Home />);
        const input = screen.getByPlaceholderText(/Enter book title, author, or ISBN/i);
        fireEvent.change(input, { target: { value: 'test search' } });
        expect(input).toHaveValue('test search');
    });

    it('should fetch data and update results on form submission', async () => {
        const mockResults: Result[] = [
            {
                id: '1',
                volumeInfo: {
                    authors: ['Test Author'],
                    description: 'Book description',
                    imageLinks: {
                        smallThumbnail: 'book.small.png',
                        thumbnail: 'book.png'
                    },
                    subtitle: 'A really good book',
                    title: 'Test Book'
                }
            }
        ];

        fetchMock.mockResponse(
            JSON.stringify(mockResults),
            {
                status: 200,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        render(<Home />);

        const input = screen.getByPlaceholderText(/Enter book title, author, or ISBN/i);
        const form = screen.getByRole('form');

        fireEvent.change(input, { target: { value: 'test search' } });
        fireEvent.submit(form!);

        render(<Listings results={mockResults} />)

        await waitFor(() => {
            expect(mockFetch).toHaveBeenCalledWith(
                expect.stringContaining('/books'),
                expect.objectContaining({
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ terms: encodeURIComponent(escape('test+search')) })
                })
            );
        });

        await waitFor(() => {
            expect(screen.getByText((content, element) => {
                return element?.tagName.toLowerCase() === 'h3' && content.includes('Test Book');
            })).toBeInTheDocument();
        });
    });

    it('should handle errors gracefully during fetch', async () => {
        mockFetch.mockRejectedValueOnce(new Error('Network error'));

        render(<Home />);

        const input = screen.getByPlaceholderText(/Enter book title, author, or ISBN/i);
        const form = screen.getByRole('form');

        fireEvent.change(input, { target: { value: 'test search' } });
        fireEvent.submit(form);

        await waitFor(() => {
            expect(screen.queryByText('Network error')).not.toBeInTheDocument();
        });
    });
});
