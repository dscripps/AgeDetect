//
//  CaptureConfirmViewController.m
//  AG02
//
//  Created by デービット スクリプス on 8/3/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//
#import "CaptureConfirmViewController.h"
#import "ASIFormDataRequest.h"
//#import "SBJson.h"
#import "FaceCaptureViewController.h"
#import "ResultsViewController.h"


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
    
    [againButton setTitle:NSLocalizedString(@"Again", @"") forState:UIControlStateNormal];
    [againButton setTitle:NSLocalizedString(@"Again", @"") forState:UIControlStateHighlighted];
    [againButton setTitle:NSLocalizedString(@"Again", @"") forState:UIControlStateDisabled];
    [againButton setTitle:NSLocalizedString(@"Again", @"") forState:UIControlStateSelected];
    [submitButton setTitle:NSLocalizedString(@"Submit", @"") forState:UIControlStateNormal];
    [submitButton setTitle:NSLocalizedString(@"Submit", @"") forState:UIControlStateHighlighted];
    [submitButton setTitle:NSLocalizedString(@"Submit", @"") forState:UIControlStateDisabled];
    [submitButton setTitle:NSLocalizedString(@"Submit", @"") forState:UIControlStateSelected];
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
    faceImage = [img retain];
    // scaling set to 2.0 makes the image 1/2 the size. 
    UIImage *scaledImage = [UIImage imageWithCGImage:[faceImage CGImage] scale:1.0 orientation:UIImageOrientationLeftMirrored];
    //UIImage *scaledImage = [UIImage imageWithCGImage:[faceImage CGImage] scale:10 orientation:UIImageOrientationLeftMirrored];
    
    //crop image
    CGRect cropRect = CGRectMake(0,0,100,100);
    CGImageRef imageRef = CGImageCreateWithImageInRect([scaledImage CGImage], cropRect);
    // or use the UIImage wherever you like
    UIImage *croppedImage = [UIImage imageWithCGImage:imageRef];
    CGImageRelease(imageRef);
    
    CGSize screenSize = [[UIScreen mainScreen] bounds].size;
    
    UIImageView *myImageView = [[UIImageView alloc] initWithImage:scaledImage];
    [myImageView setFrame:CGRectMake(screenSize.width*0.20, 100, screenSize.width*0.60, screenSize.height*0.60)];
    
    //CGAffineTransform rotate = CGAffineTransformMakeRotation(1.57079633);
    //[myImageView setTransform:rotate];
    
    [self.view addSubview:myImageView];
    [myImageView release];
    
    last_camera = camera;
}


- (void)showProgressIndicator:(NSString *)text {
	//[UIApplication sharedApplication].networkActivityIndicatorVisible = YES;
	self.view.userInteractionEnabled = FALSE;
	/*if(!progressHUD) {
		CGFloat w = 160.0f, h = 120.0f;
		progressHUD = [[UIProgressHUD alloc] initWithFrame:CGRectMake((self.view.frame.size.width-w)/2, (self.view.frame.size.height-h)/2, w, h)];
		[progressHUD setText:text];
		[progressHUD showInView:self.view];
	}*/
    [MBProgressHUD showHUDAddedTo:self.view animated:YES];
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
    
    
	/*
	 turning the image into a NSData object
	 getting the image back out of the UIImageView
	 setting the quality to 90
     */
	// setting up the URL to post to
	NSString *urlString = @"http://ec2-176-34-8-245.ap-northeast-1.compute.amazonaws.com/upload/";
    
    NSString *uuid = [[NSUserDefaults standardUserDefaults] stringForKey:@"uuid"];
    NSString *uuid_jpg = [NSString stringWithFormat:@"%@", uuid];
    
    NSString *language = [[NSLocale preferredLanguages] objectAtIndex:0];
    
    //NSLog(@"id is %@", [[NSUserDefaults standardUserDefaults] stringForKey:@"uuid"]);
    ASIFormDataRequest *request = [ASIFormDataRequest requestWithURL:[NSURL URLWithString:urlString]];
    [request setRequestMethod:@"POST"];
    [request setPostValue:uuid forKey:@"udid"];
    [request setPostValue:language forKey:@"language"];
    [request setData:UIImageJPEGRepresentation(faceImage, 1.0f) withFileName:uuid_jpg andContentType:@"image/jpeg" forKey:@"image"];
    [request setDelegate:self];
    [request startAsynchronous];
    [self showProgressIndicator:@"Loading"];
    
}

- (void)requestFinished:(ASIHTTPRequest *)request
{
    NSLog(@"finished");
    // Use when fetching text data
    NSString *responseString = [request responseString];
    
    // Use when fetching binary data
    //NSData *responseData = [request responseData];
    
    //NSLog(responseString);
    
    NSDictionary *responseDict = [responseString JSONValue];
    if (responseDict == NULL) {
        [self reportError];
        return;
    }
    
    NSString *age = [responseDict valueForKey:@"age"];
    //save results for use later in the app
    [[NSUserDefaults standardUserDefaults] setObject:age forKey:@"age"];
    [[NSUserDefaults standardUserDefaults] setObject:[responseDict valueForKey:@"message_forehead"] forKey:@"message_forehead"];
    [[NSUserDefaults standardUserDefaults] setObject:[responseDict valueForKey:@"message_left_eye"] forKey:@"message_left_eye"];
    [[NSUserDefaults standardUserDefaults] setObject:[responseDict valueForKey:@"message_right_eye"] forKey:@"message_right_eye"];
    [[NSUserDefaults standardUserDefaults] setObject:[responseDict valueForKey:@"message_nose_mouth"] forKey:@"message_nose_mouth"];
    //NSLog(@"%@",age);
    
    ResultsViewController *cV = [[[ResultsViewController alloc] initWithNibName:@"ResultsViewController" bundle:nil] autorelease];
    cV.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:cV animated:YES];
    [self viewDidUnload];
}

- (void) reportError {
    //server side error
    UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"ERROR" 
                                                    message:@"Please try again" 
                                                   delegate:self 
                                          cancelButtonTitle:@"OK"
                                          otherButtonTitles:nil];
    [alert show];
    [alert release];
}
- (void)alertView:(UIAlertView *)alertView clickedButtonAtIndex:(NSInteger)buttonIndex {
    NSLog(@"%d", buttonIndex);
    NSLog(@"alert closed!");
    [self againButton:nil];
}




@end
