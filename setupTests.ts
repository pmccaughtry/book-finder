import '@testing-library/jest-dom';
import fetchMock from 'jest-fetch-mock';
import { TextEncoder, TextDecoder as NodeTextDecoder } from 'util';

global.TextEncoder = TextEncoder;
global.TextDecoder = NodeTextDecoder as unknown as { new(): TextDecoder };

fetchMock.enableMocks();
