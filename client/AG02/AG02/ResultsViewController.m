//
//  ResultsViewController.m
//  AG02
//
//  Created by デービット スクリプス on 8/2/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "ResultsViewController.h"
#import "ViewController.h"
#import "DetailsViewController.h"
#import "AboutViewController.h"

@interface ResultsViewController ()

@end

@implementation ResultsViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    // Do any additional setup after loading the view from its nib.
    //NSLog(@"here!");
    //NSLog(@"%@", [[NSUserDefaults standardUserDefaults] stringForKey:@"age"]);
    //set age
    ageLabel.text = [[NSUserDefaults standardUserDefaults] stringForKey:@"age"];
    
    
    result.text = NSLocalizedString(@"Result", @"");
    yearsOld.text = NSLocalizedString(@"Years Old", @"");
    [okButton setTitle:NSLocalizedString(@"Back", @"") forState:UIControlStateNormal];
    [okButton setTitle:NSLocalizedString(@"Back", @"") forState:UIControlStateHighlighted];
    [okButton setTitle:NSLocalizedString(@"Back", @"") forState:UIControlStateDisabled];
    [okButton setTitle:NSLocalizedString(@"Back", @"") forState:UIControlStateSelected];
    
    [aboutButton setTitle:NSLocalizedString(@"About", @"") forState:UIControlStateNormal];
    [aboutButton setTitle:NSLocalizedString(@"About", @"") forState:UIControlStateHighlighted];
    [aboutButton setTitle:NSLocalizedString(@"About", @"") forState:UIControlStateDisabled];
    [aboutButton setTitle:NSLocalizedString(@"About", @"") forState:UIControlStateSelected];
    
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

//MARK: IBactions
- (IBAction)okButton:(id)sender
{
    ViewController *cV = [[[ViewController alloc] initWithNibName:@"ViewController_iPhone" bundle:nil] autorelease];
    cV.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:cV animated:YES];
    [self viewDidUnload];
}

- (IBAction)aboutButton:(id)sender
{
    AboutViewController *cV = [[[AboutViewController alloc] initWithNibName:@"AboutViewController" bundle:nil] autorelease];
    cV.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:cV animated:YES];
    [self viewDidUnload];
}


- (void)openNewView
{
    
    DetailsViewController *cV = [[[DetailsViewController alloc] initWithNibName:@"DetailsViewController" bundle:nil] autorelease];
    cV.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:cV animated:YES];
    [cV initStuff:currentPart];
    //[cV initStuff:@"forehead"];
    [self viewDidUnload];
    
}


- (void) openDetails:(NSString*)part {
    
    currentPart = part;
    [self showProgressIndicator:@"Loading"];
    //[self performSelectorInBackground:@selector(openNewView) withObject:nil];
	//[self performSelectorOnMainThread:@selector(openNewView) withObject:nil waitUntilDone:NO];
    //[self performSelector:@selector(openNewView) withObject:nil];
    //[self performSelector: afterDelay:1 inModes:nil];
    [self performSelector:@selector(openNewView) withObject:nil afterDelay:1.0];

}



- (IBAction)foreheadButton:(id)sender {
    [self openDetails:@"forehead"];
}

- (IBAction)leftEyeButton:(id)sender {
    [self openDetails:@"left_eye"];
}

- (IBAction)rightEyeButton:(id)sender {
    [self openDetails:@"right_eye"];
}

- (IBAction)mouthButton:(id)sender {
    [self openDetails:@"nose_mouth"];
    //[self openDetails:@"face_aligned"];
}



@end
