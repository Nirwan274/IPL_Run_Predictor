import { Component } from '@angular/core';
import { IplService } from 'src/app/ipl.service';

@Component({
  selector: 'app-dash',
  templateUrl: './dash.component.html',
  styleUrls: ['./dash.component.css']
})
export class DashComponent {
  strikerName: string = '';
  bowlerName: string = '';
  ball: number = 0;
  predictedRuns: number | null = null;
  errorMessage: string | null = null;
  maxOvers: number = 20.0;

  constructor(private iplService: IplService) {}

  Prediction() {
    if (this.ball > this.maxOvers) {
      this.errorMessage = 'There are only 20 overs in a match.';
      this.predictedRuns = null;
    } else {
      this.iplService.getPrediction(this.strikerName, this.bowlerName, this.ball).subscribe(
        prediction => {
          this.predictedRuns = prediction;
          this.errorMessage = null;
        },
        error => {
          console.error('Error making prediction:', error);
          this.errorMessage = 'An error occurred while making the prediction.';
          this.predictedRuns = null;
        }
      );
    }
  }
}
