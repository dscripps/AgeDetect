//
//  CaptureConfirmViewController.m
//  AG02
//
//  Created by デービット スクリプス on 8/3/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "CaptureConfirmViewController.h"
#import "FaceCaptureViewController.h"

@interface CaptureConfirmViewController ()

@end

@implementation CaptureConfirmViewController

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
    //[self showProgressIndicator:@"Processing"];
    [super viewDidLoad];
    // Do any additional setup after loading the view from its nib.
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

// MARK: showing image

- (void)initStuff:(UIImage *)img camera:(int)camera {
    
    
    // scaling set to 2.0 makes the image 1/2 the size. 
    UIImage *scaledImage = [UIImage imageWithCGImage:[img CGImage] scale:1.0 orientation:UIImageOrientationLeftMirrored];
    
    CGSize screenSize = [[UIScreen mainScreen] bounds].size;
    
    UIImageView *myImageView = [[UIImageView alloc] initWithImage:scaledImage];
    [myImageView setFrame:CGRectMake(screenSize.width*0.125, 6, screenSize.width*0.75, screenSize.height*0.75)];
    
    //CGAffineTransform rotate = CGAffineTransformMakeRotation(1.57079633);
    //[myImageView setTransform:rotate];
    
    [self.view addSubview:myImageView];
    [myImageView release];
    
    last_camera = camera;
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

// MARK: IBActions

// again button
- (IBAction)againButton:(id)sender
{
    [self showProgressIndicator:@"Loading"];
	[self performSelectorInBackground:@selector(openAgainView) withObject:nil];
}

- (void)openAgainView 
{
    FaceCaptureViewController *captureView = [[[FaceCaptureViewController alloc] initWithNibName:@"FaceCaptureViewController" bundle:nil] autorelease];
    captureView.camera = last_camera;
    captureView.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:captureView animated:YES];
    [self viewDidUnload];
}

- (IBAction)submitButton:(id)sender
{
    NSLog(@"submit me!");
    
    //http://zcentric.com/2008/08/
}


@end
