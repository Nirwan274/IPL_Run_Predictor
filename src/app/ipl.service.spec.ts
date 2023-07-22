import { TestBed } from '@angular/core/testing';

import { IplService } from './ipl.service';

describe('IplService', () => {
  let service: IplService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(IplService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
