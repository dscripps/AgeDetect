//
//  DirectionsViewController.m
//  AG02
//
//  Created by デービット スクリプス on 8/1/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "DirectionsViewController.h"
#import "FaceCaptureViewController.h"

@interface DirectionsViewController ()

@end

@implementation DirectionsViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    // Do any additional setup after loading the view from its nib.
    
    // Create a view of the standard size at the bottom of the screen.
    // Available AdSize constants are explained in GADAdSize.h.
    //bannerView_ = [[GADBannerView alloc] initWithAdSize:kGADAdSizeBanner];
    // Initialize the banner at the bottom of the screen.
    //CGPoint origin = CGPointMake(0.0, self.view.frame.size.height + 20 - CGSizeFromGADAdSize(kGADAdSizeBanner).height);
    CGPoint origin = CGPointMake(0.0, self.view.frame.size.height - 50);
    
    // Use predefined GADAdSize constants to define the GADBannerView.
    bannerView_ = [[GADBannerView alloc] initWithAdSize:kGADAdSizeBanner origin:origin];
    
    // Specify the ad's "unit identifier." This is your AdMob Publisher ID.
    bannerView_.adUnitID = @"a1504f4c90f2afe";
    
    // Let the runtime know which UIViewController to restore after taking
    // the user wherever the ad goes and add it to the view hierarchy.
    bannerView_.rootViewController = self;
    [self.view addSubview:bannerView_];
    
    // Initiate a generic request to load it with an ad.
    [bannerView_ loadRequest:[GADRequest request]];
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

// MARK: IBActions

// ok button
- (IBAction)okButton:(id)sender
{
    [self showProgressIndicator:@"Loading"];
	[self performSelectorInBackground:@selector(openNewView) withObject:nil];
    
    //NSLog(@"OK PRESSED!");
}

- (void)openNewView 
{
    FaceCaptureViewController *captureView = [[[FaceCaptureViewController alloc] initWithNibName:@"FaceCaptureViewController" bundle:nil] autorelease];
    captureView.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    //[self presentModalViewController:captureView animated:YES];
    [self presentModalViewController:captureView animated:YES];
    //[self dismissModalViewControllerAnimated:YES];
    [self viewDidUnload];
    
}

- (void)showProgressIndicator:(NSString *)text {
	//[UIApplication sharedApplication].networkActivityIndicatorVisible = YES;
	self.view.userInteractionEnabled = FALSE;
	if(!progressHUD) {
		CGFloat w = 160.0f, h = 120.0f;
		progressHUD = [[UIProgressHUD alloc] initWithFrame:CGRectMake((self.view.frame.size.width-w)/2, (self.view.frame.size.height-h)/2, w, h)];
		[progressHUD setText:text];
		[progressHUD showInView:self.view];
	}
}

@end
