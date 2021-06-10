import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChartlistComponent } from './chartlist.component';

describe('ChartlistComponent', () => {
  let component: ChartlistComponent;
  let fixture: ComponentFixture<ChartlistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChartlistComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChartlistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
